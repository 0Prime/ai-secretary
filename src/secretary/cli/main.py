import subprocess
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
import typer
from typing_extensions import Annotated

from secretary import settings, manager, video_analyzer, vault
from secretary.enums import MaterialType
from secretary.database import db


app = typer.Typer(
    name="secretary",
    help="AI Secretary for Obsidian knowledge base management",
    add_completion=False,
)

console = Console()


def safe_text(text: str, max_len: int = 200) -> str:
    if not text:
        return "-"
    text = text[:max_len]
    try:
        text.encode('cp1252')
        return text
    except UnicodeEncodeError:
        return text.encode('ascii', 'replace').decode('ascii')


@app.command()
def add(
    source: str = typer.Argument(..., help="URL or path to add"),
    type: MaterialType = typer.Option(
        MaterialType.VIDEO,
        "--type",
        "-t",
        help="Material type",
    ),
    title: Optional[str] = typer.Option(None, "--title", help="Custom title"),
):
    try:
        material = manager.add_material(source, type, title)
        console.print(f"[green]Added material:[/green] {material.id}")
        console.print(f"  Title: {material.title}")
        console.print(f"  Type: {material.type}")
        console.print(f"  Status: {material.status}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")


@app.command()
def list_materials(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    limit: int = typer.Option(20, "--limit", "-l", help="Max results"),
):
    materials = manager.list_materials(status=status, limit=limit)
    
    if not materials:
        console.print("[yellow]No materials found[/yellow]")
        return
    
    table = Table(title=f"Materials ({len(materials)} results)")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Type", style="magenta")
    table.add_column("Status", style="yellow")
    table.add_column("Novelty", justify="right")
    
    for m in materials:
        novelty = f"{m.novelty_score:.2f}" if m.novelty_score else "ΓÇö"
        table.add_row(
            m.id[:8],
            m.title[:40],
            m.type,
            m.status,
            novelty,
        )
    
    console.print(table)


@app.command()
def status(
    material_id: str = typer.Argument(..., help="Material ID"),
):
    material = manager.get_material(material_id)
    
    if not material:
        console.print(f"[red]Material not found:[/red] {material_id}")
        raise typer.Exit(1)
    
    novelty_str = f"{material.novelty_score:.2f}" if material.novelty_score else "-"
    info = f"""[bold]Material Details[/bold]

ID: {material.id}
Title: {safe_text(material.title)}
Type: {material.type}
Status: {material.status}
URL: {safe_text(material.source_url) if material.source_url else '-'}
Novelty Score: {novelty_str}
Added: {material.added_at.strftime('%Y-%m-%d %H:%M')}
"""
    
    if material.tags:
        info += f"Tags: {safe_text(', '.join(material.tags))}\n"
    
    if material.summary:
        info += f"\n[bold]Summary:[/bold]\n{safe_text(material.summary, 300)}...\n"
    
    if material.video_metadata:
        vm = material.video_metadata
        info += f"\n[bold]Video Info:[/bold]\n"
        if vm.channel:
            info += f"Channel: {safe_text(vm.channel)}\n"
        if vm.duration:
            mins, secs = divmod(vm.duration, 60)
            info += f"Duration: {mins}:{secs:02d}\n"
        if vm.chapters:
            info += f"Chapters: {len(vm.chapters)}\n"
    
    recommendation = manager.get_novelty_recommendation(material_id)
    info += f"\n[bold green]Recommendation:[/bold green] {safe_text(recommendation)}"
    
    console.print(Panel(info, title=f"Material {material_id[:8]}"))


@app.command()
def analyze(
    material_id: str = typer.Argument(..., help="Material ID"),
):
    material = manager.get_material(material_id)
    
    if not material:
        console.print(f"[red]Material not found:[/red] {material_id}")
        raise typer.Exit(1)
    
    console.print(f"[cyan]Analyzing:[/cyan] {material.title}")
    
    if material.type == "video":
        with console.status("[cyan]Analyzing video..."):
            material = video_analyzer.analyze_video(material_id)
            db.update_material(material)
    
    with console.status("[cyan]Computing novelty and tags..."):
        material = manager.analyze_material(material_id)
    
    console.print(f"[green]Analysis complete![/green]")
    console.print(f"Novelty score: {material.novelty_score:.2f}")
    console.print(f"Tags: {safe_text(', '.join(material.tags))}")
    console.print(f"Recommendation: {safe_text(manager.get_novelty_recommendation(material_id))}")
    
    if material.summary:
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(safe_text(material.summary, 300))


@app.command()
def learn(
    material_id: str = typer.Argument(..., help="Material ID"),
    sync: bool = typer.Option(True, "--sync/--no-sync", help="Sync to Obsidian"),
):
    material = manager.mark_as_learned(material_id)
    console.print(f"[green]Marked as learned:[/green] {material.title}")
    
    if sync:
        with console.status("[cyan]Syncing to Obsidian..."):
            path = vault.sync_material(material_id)
        if path:
            console.print(f"Created: {path}")


@app.command()
def reindex():
    pending = manager.list_materials(status="pending")
    
    if not pending:
        console.print("[yellow]No pending materials[/yellow]")
        return
    
    console.print(f"[cyan]Reindexing {len(pending)} materials...[/cyan]")
    
    for m in pending:
        try:
            manager.analyze_material(m.id)
            console.print(f"  [green]Γ£ô[/green] {m.title[:40]}")
        except Exception as e:
            console.print(f"  [red]Γ£ù[/red] {m.title[:40]}: {e}")


@app.command()
def video_summarize(
    url: str = typer.Argument(..., help="YouTube URL"),
):
    with console.status("[cyan]Getting transcript and summarizing..."):
        summary = video_analyzer.summarize_video(url)
    
    console.print(Panel(summary, title="Video Summary"))


@app.command()
def video_chapters(
    url: str = typer.Argument(..., help="YouTube URL"),
):
    chapters = video_analyzer.get_chapters(url)
    
    if not chapters:
        console.print("[yellow]No chapters found[/yellow]")
        return
    
    table = Table(title="Video Chapters")
    table.add_column("Time", style="cyan")
    table.add_column("Title", style="white")
    
    for ch in chapters:
        mins, secs = divmod(ch.time, 60)
        table.add_row(f"{mins}:{secs:02d}", ch.title)
    
    console.print(table)


@app.command()
def video_find(
    url: str = typer.Argument(..., help="YouTube URL"),
    query: str = typer.Argument(..., help="Search query"),
):
    with console.status(f"[cyan]Finding relevant parts for '{query}'...[/cyan]"):
        parts = video_analyzer.find_relevant_parts(url, query)
    
    if not parts:
        console.print("[yellow]No relevant parts found[/yellow]")
        return
    
    console.print(f"[green]Found {len(parts)} relevant parts:[/green]\n")
    
    for seconds, text in parts:
        mins, secs = divmod(seconds, 60)
        console.print(f"[cyan]{mins}:{secs:02d}[/cyan] ΓÇö {text[:100]}")


@app.command()
def add_from_tabs(
    filter_pattern: Optional[str] = typer.Option(
        None, "--filter", "-f", help="Filter URL pattern"
    ),
):
    added = 0
    
    # Try brotab first
    try:
        result = subprocess.run(
            ["python", "-c", "from brotab.main import main; main()", "--", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            
            for line in lines:
                if '\t' in line:
                    tab_id, url, title = line.split('\t', 2)
                    
                    if filter_pattern and filter_pattern not in url:
                        continue
                    
                    if 'youtube.com' in url or 'youtu.be' in url:
                        try:
                            manager.add_material(url, MaterialType.VIDEO, title)
                            added += 1
                            console.print(f"[green]+[/green] {title[:50]}")
                        except ValueError:
                            console.print(f"[yellow]├[/yellow] Already exists: {title[:40]}")
            
            if added > 0:
                console.print(f"\n[green]Added {added} videos from brotab tabs[/green]")
                return
    except Exception as e:
        pass
    
    # Fallback: try browser_history
    try:
        import browser_history
        from browser_history.browsers import Chrome, Firefox
        
        for browser_cls in [Chrome, Firefox]:
            try:
                browser = browser_cls()
                history = browser.fetch_history()
                histories = history.histories
                
                seen = set()
                for h in histories:
                    url = h[1]
                    if url in seen:
                        continue
                    seen.add(url)
                    
                    if filter_pattern and filter_pattern not in url:
                        continue
                    
                    if 'youtube.com' in url or 'youtu.be' in url:
                        title = url
                        try:
                            manager.add_material(url, MaterialType.VIDEO, title)
                            added += 1
                            console.print(f"[green]+[/green] {url[:50]}")
                        except ValueError:
                            pass
                
                if added > 0:
                    console.print(f"\n[green]Added {added} videos from browser history[/green]")
                    return
            except:
                continue
    except ImportError:
        pass
    
    console.print("[yellow]No tabs available. Options:[/yellow]")
    console.print("  1. Install brotab browser extension: https://github.com/balta2ar/brotab")
    console.print("  2. Or install browser-history: pip install browser-history")


@app.command()
def sync(
    material_id: str = typer.Argument(..., help="Material ID"),
):
    path = vault.sync_material(material_id)
    
    if path:
        console.print(f"[green]Synced to:[/green] {path}")
    else:
        console.print("[red]Failed to sync[/red]")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
):
    materials = manager.list_materials(status="learned", limit=50)
    
    results = [m for m in materials if query.lower() in m.title.lower()]
    
    if not results:
        console.print("[yellow]No results found[/yellow]")
        return
    
    console.print(f"[green]Found {len(results)} results:[/green]\n")
    
    for m in results:
        console.print(f"[cyan]{m.title[:60]}[/cyan]")
        if m.tags:
            console.print(f"  Tags: {', '.join(m.tags[:5])}")


@app.command()
def query(
    query_text: str = typer.Argument(..., help="Query to search in knowledge base"),
    limit: int = typer.Option(5, "--limit", "-n", help="Number of results"),
):
    """Query your knowledge base for learned materials."""
    from secretary.material_manager import MaterialManager
    mgr = MaterialManager()
    
    results = mgr.query_knowledge_base(query_text, limit=limit)
    
    if not results:
        console.print("[yellow]No matching materials found in knowledge base[/yellow]")
        return
    
    console.print(f"[green]Found {len(results)} related materials:[/green]\n")
    
    for m in results:
        console.print(f"[cyan]{m.title[:60]}[/cyan]")
        if m.tags:
            console.print(f"  Tags: {', '.join(m.tags[:5])}")
        if m.novelty_score is not None:
            console.print(f"  Novelty: {m.novelty_score:.2f}")
        console.print()


@app.command()
def recommend(
    limit: int = typer.Option(5, "--limit", "-n", help="Number of recommendations"),
):
    """Get recommended materials to learn next."""
    from secretary.material_manager import MaterialManager
    mgr = MaterialManager()
    
    results = mgr.get_learning_recommendations(limit=limit)
    
    if not results:
        console.print("[yellow]No pending materials to recommend[/yellow]")
        console.print("Try: secretary add <url>")
        return
    
    console.print(f"[green]Recommended materials (by novelty):[/green]\n")
    
    for m in results:
        rec = mgr.get_novelty_recommendation(m.id)
        console.print(f"[cyan]{m.title[:60]}[/cyan]")
        console.print(f"  Novelty: {m.novelty_score:.2f} | Recommendation: {rec}")
        console.print()


@app.command()
def related(
    material_id: str = typer.Argument(..., help="Material ID to find related"),
    limit: int = typer.Option(5, "--limit", "-n", help="Number of related items"),
):
    """Find related materials by tags."""
    from secretary.material_manager import MaterialManager
    mgr = MaterialManager()
    
    results = mgr.find_relatedMaterials(material_id, limit=limit)
    
    if not results:
        console.print("[yellow]No related materials found[/yellow]")
        return
    
    console.print(f"[green]Related materials:[/green]\n")
    
    for m in results:
        common = set(m.tags or []) & set(results[0].tags or []) if results else set()
        console.print(f"[cyan]{m.title[:60]}[/cyan]")
        console.print(f"  Common tags: {', '.join(common)}")
        console.print()


@app.command()
def compare(
    item1: str = typer.Argument(..., help="First item to compare"),
    item2: str = typer.Argument(..., help="Second item to compare"),
    criteria: Optional[str] = typer.Option(None, "--criteria", "-c", help="Comparison criteria"),
):
    """Compare two items (tools, approaches, products, etc.)."""
    from secretary.ai_router import AIRouter
    router = AIRouter()
    
    prompt = f"""Compare these two items:

{item1} vs {item2}

{f'Criteria: {criteria}' if criteria else 'Compare on: features, pros, cons, use cases.'}

Provide a clear comparison table and summary."""

    with console.status("[cyan]Analyzing...[/cyan]"):
        result, provider = router.complete_with_fallback(prompt)
    
    console.print(Panel(result, title=f"{item1} vs {item2}"))


@app.command()
def research(
    topic: str = typer.Argument(..., help="Topic to research"),
    depth: str = typer.Option("brief", "--depth", "-d", help="brief, medium, or detailed"),
):
    """Research a topic and provide key insights."""
    from secretary.ai_router import AIRouter
    router = AIRouter()
    
    depth_instructions = {
        "brief": "Provide 3-5 key points in 100 words.",
        "medium": "Provide 5-7 key points with brief explanations in 300 words.",
        "detailed": "Provide comprehensive overview in 600 words with examples.",
    }
    
    prompt = f"""Research: {topic}

{depth_instructions.get(depth, depth_instructions['brief'])}

Format:
- Key points
- Main takeaways
- Practical applications"""

    with console.status(f"[cyan]Researching {topic}...[/cyan]"):
        result, provider = router.complete_with_fallback(prompt)
    
    console.print(Panel(result, title=f"Research: {topic}"))


@app.command()
def ask(
    query: str = typer.Argument(..., help="Question to ask AI agent"),
    provider: Optional[str] = typer.Option(
        None,
        "--provider",
        "-p",
        help="AI provider (auto-selects best if not specified)"
    ),
):
    """Ask AI agent a question. Auto-selects best available provider."""
    from secretary.ai_router import AIRouter
    router = AIRouter()
    
    with console.status(f"[cyan]Thinking...[/cyan]"):
        try:
            result, used_provider = router.complete_with_fallback(
                query,
                preferred_provider=provider
            )
            console.print(f"[green]Provider:[/green] {used_provider}\n")
            console.print(result)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


@app.command()
def providers(
    show_all: bool = typer.Option(
        False,
        "--all",
        help="Show all providers even if not working"
    ),
):
    """Show available AI providers."""
    from secretary.ai_router import AIRouter
    router = AIRouter()
    
    if show_all:
        console.print("[cyan]All configured providers:[/cyan]")
        for name in router.provider_priority:
            status = "[green]OK[/green]" if name in router.providers else "[red]MISSING[/red]"
            console.print(f"  {status} {name}")
    else:
        available = router.get_available_providers()
        best = router.get_best_provider()
        
        console.print("[cyan]Available providers:[/cyan]")
        for p in available:
            marker = " <- best" if p == best else ""
            console.print(f"  [green]OK[/green] {p}{marker}")
        
        if not available:
            console.print("[red]No providers available![/red]")


@app.command()
def init():
    console.print("[cyan]Initializing Secretary database...[/cyan]")
    
    settings.secretary_data_path.mkdir(parents=True, exist_ok=True)
    db.engine
    
    console.print(f"[green]Database created at:[/green]")
    console.print(f"  {settings.secretary_db_path}")
    console.print(f"\n[green]Vector DB path:[/green]")
    console.print(f"  {settings.secretary_vector_path}")


if __name__ == "__main__":
    app()
