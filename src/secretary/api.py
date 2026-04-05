#!/usr/bin/env python
"""
Simple API server for AI Secretary.
Allows other applications to call AI Secretary functions via HTTP.
"""

import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, 'src')

from secretary.ai_router import AIRouter
from secretary.material_manager import MaterialManager
from secretary import settings, manager, video_analyzer, vault


class AISecretaryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        router = AIRouter()
        
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            
        elif path == '/providers':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            providers = router.get_available_providers()
            best = router.get_best_provider()
            self.wfile.write(json.dumps({
                'available': providers,
                'best': best
            }).encode())
            
        elif path == '/ask':
            question = query.get('q', [''])[0]
            if not question:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing q parameter'}).encode())
                return
            
            try:
                result, provider = router.complete_with_fallback(question)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'answer': result,
                    'provider': provider
                }).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                
        elif path == '/recommend':
            mgr = MaterialManager()
            results = mgr.get_learning_recommendations(limit=5)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            data = [{
                'id': m.id,
                'title': m.title,
                'novelty': m.novelty_score,
                'tags': m.tags
            } for m in results]
            
            self.wfile.write(json.dumps(data).encode())
            
        elif path == '/query':
            query_text = query.get('q', [''])[0]
            if not query_text:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing q parameter'}).encode())
                return
            
            mgr = MaterialManager()
            results = mgr.query_knowledge_base(query_text, limit=10)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            data = [{
                'id': m.id,
                'title': m.title,
                'tags': m.tags,
                'summary': m.summary[:200] if m.summary else None
            } for m in results]
            
            self.wfile.write(json.dumps(data).encode())
            
        elif path == '/materials':
            mgr = MaterialManager()
            materials = mgr.list_materials(limit=50)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            data = [{
                'id': m.id,
                'title': m.title,
                'status': m.status,
                'novelty': m.novelty_score
            } for m in materials]
            
            self.wfile.write(json.dumps(data).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def log_message(self, format, *args):
        print(f"[API] {format % args}")


def run_server(port: int = 8765):
    server = HTTPServer(('localhost', port), AISecretaryHandler)
    print(f"AI Secretary API running on http://localhost:{port}")
    print("Endpoints:")
    print(f"  GET /health          - Health check")
    print(f"  GET /providers       - Available AI providers")
    print(f"  GET /ask?q=...       - Ask AI question")
    print(f"  GET /recommend       - Learning recommendations")
    print(f"  GET /query?q=...     - Search knowledge base")
    print(f"  GET /materials       - List all materials")
    print()
    server.serve_forever()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Secretary API Server')
    parser.add_argument('--port', '-p', type=int, default=8765, help='Port to run server on')
    args = parser.parse_args()
    
    run_server(args.port)
