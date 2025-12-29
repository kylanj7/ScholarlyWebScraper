"""
Search terms configuration for scholarly article scraper.
Organized by academic domains and research areas.
"""

def get_academic_search_terms():
    """Return comprehensive academic search terms organized by domain."""
    return {
        'artificial_intelligence': [
            'artificial intelligence machine learning',
            'deep neural networks',
            'transformer models attention mechanism',
            'computer vision image recognition',
            'natural language processing NLP',
            'reinforcement learning algorithms',
            'generative adversarial networks GAN',
            'convolutional neural networks CNN',
            'recurrent neural networks RNN',
            'BERT GPT language models',
            'federated learning distributed',
            'explainable AI XAI',
            'adversarial machine learning',
            'neural architecture search',
            'meta-learning few-shot',
            'graph neural networks GNN',
            'quantum machine learning',
            'multimodal learning',
            'transfer learning domain adaptation',
            'unsupervised representation learning'
        ],
        
        'systems_computing': [
            'distributed systems architecture',
            'cloud computing infrastructure',
            'microservices containerization',
            'kubernetes container orchestration',
            'database systems performance',
            'NoSQL distributed databases',
            'streaming data processing',
            'event-driven architecture',
            'serverless computing',
            'edge computing fog computing',
            'blockchain distributed ledger',
            'consensus algorithms distributed',
            'load balancing scalability',
            'system reliability engineering',
            'fault tolerance mechanisms',
            'performance monitoring observability',
            'cache coherence protocols',
            'memory management systems',
            'storage systems optimization',
            'network protocols optimization'
        ],
        
        'cybersecurity': [
            'network security protocols',
            'cryptography encryption algorithms',
            'intrusion detection systems',
            'malware analysis detection',
            'vulnerability assessment',
            'penetration testing methodologies',
            'blockchain security',
            'privacy-preserving technologies',
            'zero-knowledge proofs',
            'homomorphic encryption',
            'secure multiparty computation',
            'digital forensics analysis',
            'threat intelligence analysis',
            'security information event management',
            'access control mechanisms',
            'authentication authorization',
            'security in IoT devices',
            'cloud security models',
            'software security testing',
            'social engineering awareness'
        ],
        
        'data_science': [
            'data mining algorithms',
            'statistical machine learning',
            'big data analytics',
            'time series analysis',
            'predictive modeling',
            'feature engineering selection',
            'dimensionality reduction techniques',
            'clustering algorithms',
            'classification regression methods',
            'ensemble learning methods',
            'Bayesian statistical methods',
            'causal inference methods',
            'A/B testing experimental design',
            'data visualization techniques',
            'stream processing analytics',
            'graph analytics algorithms',
            'recommendation systems',
            'anomaly detection methods',
            'optimization algorithms',
            'information retrieval ranking'
        ],
        
        'hardware_systems': [
            'computer architecture design',
            'processor microarchitecture',
            'memory hierarchy optimization',
            'cache design algorithms',
            'parallel computing architectures',
            'GPU computing CUDA',
            'FPGA reconfigurable computing',
            'embedded systems design',
            'real-time systems',
            'low-power computing design',
            'thermal management electronics',
            'reliability fault tolerance hardware',
            'hardware security modules',
            'network-on-chip design',
            'quantum computing hardware',
            'neuromorphic computing',
            'optical computing systems',
            'storage systems architecture',
            'interconnect networks design',
            'power management circuits'
        ],
        
        'software_engineering': [
            'software design patterns',
            'agile software development',
            'DevOps continuous integration',
            'software testing methodologies',
            'code quality metrics',
            'software architecture patterns',
            'version control systems',
            'software maintenance evolution',
            'requirements engineering',
            'software project management',
            'API design REST GraphQL',
            'mobile application development',
            'web application frameworks',
            'software performance optimization',
            'debugging profiling tools',
            'software documentation practices',
            'open source software development',
            'software licensing models',
            'technical debt management',
            'software metrics analysis'
        ],
        
        'quantum_computing': [
            'quantum algorithms design',
            'quantum error correction',
            'quantum cryptography protocols',
            'quantum machine learning',
            'quantum simulation methods',
            'quantum hardware platforms',
            'quantum software frameworks',
            'variational quantum algorithms',
            'quantum advantage demonstrations',
            'quantum networking protocols',
            'quantum sensing metrology',
            'adiabatic quantum computing',
            'topological quantum computing',
            'quantum chemistry simulation',
            'quantum optimization problems',
            'quantum information theory',
            'quantum entanglement applications',
            'quantum decoherence mitigation',
            'hybrid quantum-classical algorithms',
            'quantum programming languages'
        ],
        
        'human_computer_interaction': [
            'user interface design principles',
            'user experience research methods',
            'accessibility universal design',
            'mobile interface design',
            'virtual reality interfaces',
            'augmented reality applications',
            'gesture recognition systems',
            'voice user interfaces',
            'brain-computer interfaces',
            'eye-tracking interaction',
            'haptic feedback systems',
            'conversational interfaces chatbots',
            'inclusive design practices',
            'usability testing methods',
            'information visualization',
            'collaborative interfaces',
            'adaptive user interfaces',
            'multimodal interaction',
            'emotion recognition interfaces',
            'social computing platforms'
        ]
    }

def get_research_methodologies():
    """Return search terms for research methodologies."""
    return {
        'experimental_methods': [
            'controlled experiments design',
            'statistical significance testing',
            'experimental validation methods',
            'reproducibility research practices',
            'peer review processes',
            'research methodology frameworks',
            'data collection protocols',
            'survey research methods',
            'case study methodologies',
            'longitudinal studies design'
        ],
        
        'evaluation_metrics': [
            'performance evaluation metrics',
            'benchmarking methodologies',
            'accuracy precision recall',
            'statistical validation methods',
            'cross-validation techniques',
            'baseline comparison methods',
            'ablation study design',
            'error analysis techniques',
            'robustness evaluation',
            'scalability testing methods'
        ]
    }

def get_academic_venues():
    """Return search terms targeting specific academic venues."""
    return {
        'top_conferences': [
            'ICML International Conference Machine Learning',
            'NeurIPS Neural Information Processing',
            'ICLR International Conference Learning Representations',
            'AAAI Artificial Intelligence Conference',
            'IJCAI International Joint Conference AI',
            'SIGCOMM Computer Communication Review',
            'OSDI Operating Systems Design Implementation',
            'SOSP Symposium Operating Systems Principles',
            'NSDI Networked Systems Design Implementation',
            'SIGMOD Database Systems Conference',
            'VLDB Very Large Data Bases',
            'WWW World Wide Web Conference',
            'CHI Computer Human Interaction',
            'USENIX Security Symposium',
            'IEEE Symposium Security Privacy',
            'CRYPTO Cryptology Conference',
            'STOC Theory of Computing',
            'FOCS Foundations Computer Science',
            'PLDI Programming Language Design Implementation',
            'ISCA Computer Architecture'
        ],
        
        'top_journals': [
            'Nature Machine Intelligence',
            'Science Robotics',
            'Journal Machine Learning Research',
            'IEEE Transactions Pattern Analysis',
            'ACM Computing Surveys',
            'Communications ACM',
            'IEEE Computer',
            'ACM Transactions Computer Systems',
            'IEEE Transactions Software Engineering',
            'ACM Transactions Database Systems',
            'IEEE Transactions Parallel Distributed',
            'Computer Networks Journal',
            'Information Systems Journal',
            'Journal Systems Software',
            'IEEE Security Privacy Magazine'
        ]
    }

# Combined function for easy access
def get_all_academic_categories():
    """Get all academic search categories combined."""
    categories = {}
    categories.update(get_academic_search_terms())
    categories.update(get_research_methodologies())
    categories.update(get_academic_venues())
    return categories

# Quick access variables
ACADEMIC_SEARCH_TERMS = get_academic_search_terms()
RESEARCH_METHODOLOGIES = get_research_methodologies()
ACADEMIC_VENUES = get_academic_venues()
ALL_CATEGORIES = get_all_academic_categories()

if __name__ == "__main__":
    # Print summary when run directly
    all_cats = get_all_academic_categories()
    total_terms = sum(len(terms) for terms in all_cats.values())
    
    print(f"Academic Search Terms Configuration")
    print(f"Total categories: {len(all_cats)}")
    print(f"Total search terms: {total_terms}")
    print("\nCategories:")
    
    for category, terms in all_cats.items():
        print(f"  - {category}: {len(terms)} terms")
