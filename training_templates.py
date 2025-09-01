TRAINING_TEMPLATES = {
    "ransomware": {
        "questions": [
            {
                "question": "What are the first three steps you should take when ransomware is detected on a system?",
                "question_type": "response",
                "difficulty": "intermediate",
                "hints": ["Think about isolation", "Consider backups", "Don't forget documentation"]
            },
            {
                "question": "How can you identify potential ransomware activity before files are encrypted?",
                "question_type": "identification", 
                "difficulty": "advanced",
                "hints": ["Monitor file system changes", "Look for unusual network traffic", "Check for suspicious processes"]
            },
            {
                "question": "What backup strategy best protects against ransomware attacks?",
                "question_type": "prevention",
                "difficulty": "beginner",
                "hints": ["Consider the 3-2-1 rule", "Think about offline storage", "Regular testing is key"]
            }
        ]
    },
    "malware": {
        "questions": [
            {
                "question": "What indicators would suggest a system is infected with malware?",
                "question_type": "identification",
                "difficulty": "beginner",
                "hints": ["Unusual network activity", "Slow performance", "Unexpected pop-ups or processes"]
            },
            {
                "question": "How would you safely analyze a suspected malware sample?",
                "question_type": "response",
                "difficulty": "advanced",
                "hints": ["Use isolated environments", "Consider dynamic analysis", "Static analysis tools"]
            }
        ]
    },
    "phishing": {
        "questions": [
            {
                "question": "What are the key red flags in an email that might indicate a phishing attempt?",
                "question_type": "identification", 
                "difficulty": "beginner",
                "hints": ["Check sender authenticity", "Look for urgency tactics", "Examine links carefully"]
            },
            {
                "question": "If a user reports clicking on a suspicious link, what immediate actions should be taken?",
                "question_type": "response",
                "difficulty": "intermediate",
                "hints": ["Isolate the system", "Change credentials", "Monitor for unusual activity"]
            }
        ]
    },
    "vulnerability_management": {
        "questions": [
            {
                "question": "What factors should you consider when prioritizing vulnerability remediation?",
                "question_type": "response",
                "difficulty": "intermediate",
                "hints": ["Consider CVSS scores", "Think about asset criticality", "Evaluate exploit availability"]
            },
            {
                "question": "How quickly should critical vulnerabilities like remote code execution flaws be patched?",
                "question_type": "prevention",
                "difficulty": "beginner",
                "hints": ["Think about emergency patching", "Consider business impact", "Reference industry standards"]
            },
            {
                "question": "What steps should be taken when a vulnerability cannot be immediately patched?",
                "question_type": "response",
                "difficulty": "advanced",
                "hints": ["Consider compensating controls", "Think about network segmentation", "Monitor for exploitation attempts"]
            }
        ]
    },
    "network_security": {
        "questions": [
            {
                "question": "What network traffic patterns might indicate a potential SMB-based attack?",
                "question_type": "identification",
                "difficulty": "intermediate",
                "hints": ["Look for unusual SMB connections", "Monitor for lateral movement", "Check for compression anomalies"]
            },
            {
                "question": "How can network segmentation help prevent the spread of wormable vulnerabilities?",
                "question_type": "prevention",
                "difficulty": "advanced",
                "hints": ["Think about broadcast domains", "Consider protocol restrictions", "Isolate critical systems"]
            },
            {
                "question": "What immediate network-level controls should be implemented when a critical protocol vulnerability is disclosed?",
                "question_type": "response",
                "difficulty": "intermediate",
                "hints": ["Consider port blocking", "Think about protocol disabling", "Monitor for scanning activity"]
            }
        ]
    },
    "general": {
        "questions": [
            {
                "question": "What is the difference between a vulnerability and an exploit?",
                "question_type": "identification",
                "difficulty": "beginner",
                "hints": ["One is a weakness", "The other takes advantage", "Think about potential vs actual"]
            },
            {
                "question": "How do you prioritize multiple security incidents occurring simultaneously?",
                "question_type": "response",
                "difficulty": "advanced", 
                "hints": ["Consider business impact", "Assess threat severity", "Available resources matter"]
            }
        ]
    }
}