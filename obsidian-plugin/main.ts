import { Plugin, TFile, Notice, Menu, Modal } from 'obsidian';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export default class AISecretaryPlugin extends Plugin {
  async onload() {
    console.log('AI Secretary plugin loaded');

    // Add ribbon icon for quick actions
    this.addRibbonIcon('brain', 'AI Secretary', () => {
      this.showQuickActionsMenu();
    });

    // Add command: Ask AI
    this.addCommand({
      id: 'ai-ask',
      name: 'Ask AI Agent',
      editorCallback: async (editor) => {
        const selected = editor.getSelection();
        await this.askAI(selected || 'Hello');
      }
    });

    // Add command: Add current note as material
    this.addCommand({
      id: 'add-current-note',
      name: 'Add Current Note to Knowledge Base',
      callback: async () => {
        const file = this.app.workspace.getActiveFile();
        if (file) {
          await this.addToKnowledgeBase(file);
        }
      }
    });

    // Add command: Analyze current note
    this.addCommand({
      id: 'analyze-current-note',
      name: 'Analyze Current Note',
      callback: async () => {
        const file = this.app.workspace.getActiveFile();
        if (file) {
          await this.analyzeNote(file);
        }
      }
    });

    // Add command: Query knowledge base
    this.addCommand({
      id: 'query-knowledge-base',
      name: 'Query Knowledge Base',
      callback: () => {
        new QueryModal(this.app, async (query) => {
          await this.queryKnowledgeBase(query);
        }).open();
      }
    });

    // Add command: Get recommendations
    this.addCommand({
      id: 'get-recommendations',
      name: 'Get Learning Recommendations',
      callback: async () => {
        await this.getRecommendations();
      }
    });

    // Add command: Compare items
    this.addCommand({
      id: 'compare-items',
      name: 'Compare Two Items',
      callback: () => {
        new CompareModal(this.app, async (item1, item2) => {
          await this.compare(item1, item2);
        }).open();
      }
    });

    // Add command: Research topic
    this.addCommand({
      id: 'research-topic',
      name: 'Research Topic',
      callback: () => {
        new ResearchModal(this.app, async (topic, depth) => {
          await this.research(topic, depth);
        }).open();
      }
    });

    // Status bar item
    this.addStatusBarItem().setText('AI Secretary Ready');
  }

  async onunload() {
    console.log('AI Secretary plugin unloaded');
  }

  showQuickActionsMenu() {
    const menu = new Menu();
    
    menu.addItem(item => item
      .setTitle('Ask AI')
      .setIcon('brain')
      .onClick(() => {
        new QueryModal(this.app, async (query) => {
          await this.askAI(query);
        }).open();
      }));
    
    menu.addItem(item => item
      .setTitle('Query Knowledge Base')
      .setIcon('search')
      .onClick(() => {
        new QueryModal(this.app, async (query) => {
          await this.queryKnowledgeBase(query);
        }).open();
      }));
    
    menu.addItem(item => item
      .setTitle('Get Recommendations')
      .setIcon('book')
      .onClick(() => this.getRecommendations()));
    
    menu.addItem(item => item
      .setTitle('Add Current Note')
      .setIcon('plus')
      .onClick(async () => {
        const file = this.app.workspace.getActiveFile();
        if (file) await this.addToKnowledgeBase(file);
      }));
    
    menu.addItem(item => item
      .setTitle('Analyze Current Note')
      .setIcon('file-digit')
      .onClick(async () => {
        const file = this.app.workspace.getActiveFile();
        if (file) await this.analyzeNote(file);
      }));
    
    menu.addItem(item => item
      .setTitle('Research Topic')
      .setIcon('library')
      .onClick(() => {
        new ResearchModal(this.app, async (topic, depth) => {
          await this.research(topic, depth);
        }).open();
      }));

    menu.showAtMouseEvent(event);
  }

  async runSecretaryCommand(args: string[]): Promise<string> {
    try {
      const { stdout } = await execAsync(`secretary ${args.join(' ')}`, {
        timeout: 120000
      });
      return stdout;
    } catch (error: any) {
      console.error('Secretary command error:', error);
      throw error;
    }
  }

  async askAI(query: string) {
    new Notice('Thinking...', 5000);
    
    try {
      const result = await this.runSecretaryCommand(['ask', query]);
      new Notice('Done!', 2000);
      
      // Create a new note with the result
      const fileName = `AI Response ${new Date().toISOString().slice(0, 10)}`;
      await this.app.vault.create(`${fileName}.md`, `# Query\n\n${query}\n\n# Response\n\n${result}`);
      
      new Notice('Response saved to new note', 3000);
    } catch (error: any) {
      new Notice(`Error: ${error.message}`, 5000);
    }
  }

  async addToKnowledgeBase(file: TFile) {
    try {
      const content = await this.app.vault.read(file);
      const frontmatter = this.getFrontmatter(content);
      const url = frontmatter?.source_url || '';
      
      if (url) {
        await this.runSecretaryCommand(['add', url, '--title', file.basename]);
        new Notice(`Added to knowledge base: ${file.basename}`, 3000);
      } else {
        new Notice('No source_url in frontmatter. Add URL to note first.', 5000);
      }
    } catch (error: any) {
      new Notice(`Error: ${error.message}`, 5000);
    }
  }

  async analyzeNote(file: TFile) {
    new Notice('Analyzing note...', 3000);
    
    try {
      // Extract URL from frontmatter
      const content = await this.app.vault.read(file);
      const frontmatter = this.getFrontmatter(content);
      const url = frontmatter?.source_url;
      
      if (url) {
        const materialId = this.getMaterialIdFromUrl(url);
        await this.runSecretaryCommand(['analyze', materialId]);
        new Notice('Analysis complete!', 3000);
      } else {
        // Just analyze the content directly
        await this.runSecretaryCommand(['analyze', file.basename]);
        new Notice('Analysis complete!', 3000);
      }
    } catch (error: any) {
      new Notice(`Error: ${error.message}`, 5000);
    }
  }

  async queryKnowledgeBase(query: string) {
    new Notice('Searching knowledge base...', 3000);
    
    try {
      const result = await this.runSecretaryCommand(['query', query]);
      
      // Create note with results
      await this.app.vault.create(
        `Query Results ${new Date().toISOString().slice(0, 10)}.md`,
        `# Query: ${query}\n\n${result}`
      );
      
      new Notice('Results saved to new note', 3000);
    } catch (error: any) {
      new Notice(`Error: ${error.message}`, 5000);
    }
  }

  async getRecommendations() {
    new Notice('Getting recommendations...', 3000);
    
    try {
      const result = await this.runSecretaryCommand(['recommend']);
      
      await this.app.vault.create(
        `Recommendations ${new Date().toISOString().slice(0, 10)}.md`,
        `# Learning Recommendations\n\n${result}`
      );
      
      new Notice('Recommendations saved', 3000);
    } catch (error: any) {
      new Notice(`Error: ${error.message}`, 5000);
    }
  }

  async compare(item1: string, item2: string) {
    new Notice('Comparing...', 3000);
    
    try {
      const result = await this.runSecretaryCommand(['compare', item1, item2]);
      
      await this.app.vault.create(
        `Compare ${item1} vs ${item2} ${new Date().toISOString().slice(0, 10)}.md`,
        `# ${item1} vs ${item2}\n\n${result}`
      );
      
      new Notice('Comparison saved', 3000);
    } catch (error: any) {
      new Notice(`Error: ${error.message}`, 5000);
    }
  }

  async research(topic: string, depth: string = 'brief') {
    new Notice('Researching...', 3000);
    
    try {
      const result = await this.runSecretaryCommand(['research', topic, '--depth', depth]);
      
      await this.app.vault.create(
        `Research ${topic} ${new Date().toISOString().slice(0, 10)}.md`,
        `# Research: ${topic}\n\n${result}`
      );
      
      new Notice('Research saved', 3000);
    } catch (error: any) {
      new Notice(`Error: ${error.message}`, 5000);
    }
  }

  getFrontmatter(content: string): Record<string, any> | null {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;
    
    const fm: Record<string, any> = {};
    const lines = match[1].split('\n');
    
    for (const line of lines) {
      const [key, ...valueParts] = line.split(':');
      if (key && valueParts.length) {
        fm[key.trim()] = valueParts.join(':').trim();
      }
    }
    
    return fm;
  }

  getMaterialIdFromUrl(url: string): string {
    // Extract video ID from YouTube URL
    const match = url.match(/(?:v=|youtu\.be\/)([\w-]+)/);
    return match ? match[1] : url;
  }
}

// Simple modal for text input
class QueryModal extends Modal {
  private onSubmit: (query: string) => void;
  private inputEl: HTMLInputElement;

  constructor(app: any, onSubmit: (query: string) => void) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: 'Ask AI Agent' });

    this.inputEl = contentEl.createEl('input', {
      type: 'text',
      placeholder: 'Enter your question...',
      cls: 'input'
    });
    this.inputEl.style.width = '100%';
    this.inputEl.style.marginBottom = '10px';

    contentEl.createEl('button', {
      text: 'Submit',
      cls: 'button'
    }).onclick = () => {
      if (this.inputEl.value) {
        this.onSubmit(this.inputEl.value);
        this.close();
      }
    };
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

class CompareModal extends Modal {
  private onSubmit: (item1: string, item2: string) => void;
  private input1: HTMLInputElement;
  private input2: HTMLInputElement;

  constructor(app: any, onSubmit: (item1: string, item2: string) => void) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: 'Compare Two Items' });

    this.input1 = contentEl.createEl('input', {
      type: 'text',
      placeholder: 'First item...',
    });
    this.input1.style.width = '100%';
    this.input1.style.marginBottom = '5px';

    this.input2 = contentEl.createEl('input', {
      type: 'text',
      placeholder: 'Second item...',
    });
    this.input2.style.width = '100%';
    this.input2.style.marginBottom = '10px';

    contentEl.createEl('button', {
      text: 'Compare',
    }).onclick = () => {
      if (this.input1.value && this.input2.value) {
        this.onSubmit(this.input1.value, this.input2.value);
        this.close();
      }
    };
  }

  onClose() {
    this.contentEl.empty();
  }
}

class ResearchModal extends Modal {
  private onSubmit: (topic: string, depth: string) => void;
  private input: HTMLInputElement;
  private select: HTMLSelectElement;

  constructor(app: any, onSubmit: (topic: string, depth: string) => void) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: 'Research Topic' });

    this.input = contentEl.createEl('input', {
      type: 'text',
      placeholder: 'Topic to research...',
    });
    this.input.style.width = '100%';
    this.input.style.marginBottom = '5px';

    this.select = contentEl.createEl('select');
    this.select.style.width = '100%';
    this.select.style.marginBottom = '10px';
    
    ['brief', 'medium', 'detailed'].forEach(d => {
      const opt = this.select.createEl('option', { value: d, text: d });
    });

    contentEl.createEl('button', {
      text: 'Research',
    }).onclick = () => {
      if (this.input.value) {
        this.onSubmit(this.input.value, this.select.value);
        this.close();
      }
    };
  }

  onClose() {
    this.contentEl.empty();
  }
}
