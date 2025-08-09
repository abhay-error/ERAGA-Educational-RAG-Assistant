import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentStructureManager:
    def __init__(self, documents_path: str = "./data/documents"):
        self.documents_path = Path(documents_path)
        self.structure_file = Path("./data/cache/document_structure.json")
        self.structure_file.parent.mkdir(parents=True, exist_ok=True)
        self.structure = self._load_structure()
    
    def _load_structure(self) -> Dict[str, Any]:
        """Load document structure from JSON file."""
        if self.structure_file.exists():
            try:
                with open(self.structure_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading document structure: {e}")
        
        return {
            "last_updated": None,
            "documents": {},
            "directories": {},
            "file_types": {},
            "keywords": {}
        }
    
    def _save_structure(self):
        """Save document structure to JSON file."""
        try:
            self.structure["last_updated"] = datetime.now().isoformat()
            with open(self.structure_file, 'w', encoding='utf-8') as f:
                json.dump(self.structure, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving document structure: {e}")
    
    def scan_documents(self) -> Dict[str, Any]:
        """Scan documents directory and update structure."""
        logger.info("Scanning documents directory...")
        
        documents = {}
        directories = {}
        file_types = {}
        keywords = {}
        
        if not self.documents_path.exists():
            logger.warning(f"Documents path does not exist: {self.documents_path}")
            return self.structure
        
        # Scan all files recursively
        for file_path in self.documents_path.rglob("*"):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(self.documents_path))
                
                # Get file info
                file_info = {
                    "name": file_path.name,
                    "path": str(file_path),
                    "relative_path": relative_path,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "type": file_path.suffix.lower(),
                    "directory": str(file_path.parent.relative_to(self.documents_path)),
                    "keywords": self._extract_keywords(file_path.name, relative_path)
                }
                
                documents[relative_path] = file_info
                
                # Track directories
                dir_path = str(file_path.parent.relative_to(self.documents_path))
                if dir_path not in directories:
                    directories[dir_path] = {
                        "path": dir_path,
                        "files": [],
                        "file_count": 0,
                        "total_size": 0
                    }
                directories[dir_path]["files"].append(relative_path)
                directories[dir_path]["file_count"] += 1
                directories[dir_path]["total_size"] += file_info["size"]
                
                # Track file types
                file_type = file_path.suffix.lower()
                if file_type not in file_types:
                    file_types[file_type] = []
                file_types[file_type].append(relative_path)
                
                # Track keywords
                for keyword in file_info["keywords"]:
                    if keyword not in keywords:
                        keywords[keyword] = []
                    if relative_path not in keywords[keyword]:
                        keywords[keyword].append(relative_path)
        
        # Update structure
        self.structure["documents"] = documents
        self.structure["directories"] = directories
        self.structure["file_types"] = file_types
        self.structure["keywords"] = keywords
        
        # Save updated structure
        self._save_structure()
        
        logger.info(f"Scanned {len(documents)} documents in {len(directories)} directories")
        return self.structure
    
    def _extract_keywords(self, filename: str, path: str) -> List[str]:
        """Extract keywords from filename and path."""
        keywords = []
        
        # Extract from filename (without extension)
        name_without_ext = Path(filename).stem.lower()
        keywords.extend(name_without_ext.split())
        
        # Extract from path
        path_parts = path.lower().split(os.sep)
        keywords.extend(path_parts)
        
        # Add common patterns
        if "module" in name_without_ext or "module" in path.lower():
            keywords.append("module")
        if "notes" in name_without_ext or "notes" in path.lower():
            keywords.append("notes")
        if "syllabus" in name_without_ext or "syllabus" in path.lower():
            keywords.append("syllabus")
        if "question" in name_without_ext or "question" in path.lower():
            keywords.append("question")
        if "bank" in name_without_ext or "bank" in path.lower():
            keywords.append("question_bank")
        
        # Remove duplicates and empty strings
        keywords = list(set([k for k in keywords if k.strip()]))
        return keywords
    
    def search_documents(self, query: str) -> List[Dict[str, Any]]:
        """Search for documents based on query."""
        query_lower = query.lower()
        results = []
        
        for doc_path, doc_info in self.structure["documents"].items():
            score = 0
            match_reasons = []
            
            # Check filename
            if query_lower in doc_info["name"].lower():
                score += 10
                match_reasons.append("filename")
            
            # Check path
            if query_lower in doc_info["relative_path"].lower():
                score += 5
                match_reasons.append("path")
            
            # Check keywords
            for keyword in doc_info["keywords"]:
                if query_lower in keyword.lower():
                    score += 3
                    match_reasons.append(f"keyword: {keyword}")
            
            # Check directory
            if query_lower in doc_info["directory"].lower():
                score += 2
                match_reasons.append("directory")
            
            if score > 0:
                results.append({
                    **doc_info,
                    "score": score,
                    "match_reasons": list(set(match_reasons))
                })
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def get_documents_by_type(self, file_type: str) -> List[Dict[str, Any]]:
        """Get all documents of a specific type."""
        file_type = file_type.lower()
        if file_type.startswith('.'):
            file_type = file_type[1:]
        
        results = []
        for doc_path, doc_info in self.structure["documents"].items():
            if doc_info["type"].lower() == file_type:
                results.append(doc_info)
        
        return results
    
    def get_documents_by_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Get all documents in a specific directory."""
        results = []
        for doc_path, doc_info in self.structure["documents"].items():
            if directory.lower() in doc_info["directory"].lower():
                results.append(doc_info)
        
        return results
    
    def get_structure_summary(self) -> Dict[str, Any]:
        """Get a summary of the document structure."""
        return {
            "total_documents": len(self.structure["documents"]),
            "total_directories": len(self.structure["directories"]),
            "file_types": {k: len(v) for k, v in self.structure["file_types"].items()},
            "last_updated": self.structure["last_updated"]
        }
