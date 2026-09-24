"""
Learning Path Module - Generates personalized structured learning path
"""
import logging
from typing import Dict
from .config import has_gemini_key, get_gemini_model_name

logger = logging.getLogger(__name__)

def _fallback_learning_path(topic: str) -> str:
    """Generate structured fallback learning path"""
    topic = topic.strip()
    
    return f"""# 📚 Personalized Learning Path: {topic}
*Generated in Fallback Mode - Configure GEMINI_API_KEY for AI-powered personalized paths*

## 🎯 Overview
This structured learning path for **{topic}** is designed to take you from beginner to advanced level with clear milestones, timelines, and resources.

---

### 🌱 Level 1: Beginner (Week 1-2)
**Goal**: Build strong fundamentals

**Topics to Cover:**
1. **Introduction to {topic}**
   - What is {topic}? Definition and importance
   - History and evolution
   - Real-world applications

2. **Core Concepts**
   - Fundamental principles of {topic}
   - Basic terminology and vocabulary
   - Simple examples and use cases

3. **Foundation Skills**
   - Basic tools and environment setup
   - First hands-on exercise
   - Common misconceptions to avoid

**Resources:**
- 📹 Videos: Search "Introduction to {topic} for beginners" on YouTube (e.g., freeCodeCamp, CrashCourse)
- 📄 Articles: Wikipedia overview + GeeksforGeeks beginner guide for {topic}
- 📚 Books: "{topic} for Dummies" or introductory chapter of standard textbook
- 💻 Practice: 5 basic exercises on {topic}

**Milestone Check:** Can you explain {topic} in simple terms to a friend?

---

### 🌿 Level 2: Intermediate (Week 3-5)
**Goal**: Deepen understanding and build practical skills

**Topics to Cover:**
1. **Intermediate Concepts**
   - Detailed mechanics of {topic}
   - How {topic} works under the hood
   - Relationships with related concepts

2. **Practical Applications**
   - Real-world case studies involving {topic}
   - Common patterns and best practices
   - Tools and frameworks associated with {topic}

3. **Hands-On Projects**
   - Mini-project 1: Apply {topic} to solve a simple problem
   - Mini-project 2: Build something using {topic}
   - Code/Implementation exercises

**Resources:**
- 📹 Videos: Intermediate tutorials - "Mastering {topic}" series
- 📄 Articles: Medium articles, official documentation for {topic}
- 📚 Books: Chapter 3-7 of standard textbook on {topic}
- 💻 Practice: 10 intermediate problems, join discussion forums (StackOverflow, Reddit r/{topic.lower().replace(' ', '')})

**Milestone Check:** Can you build a small project using {topic}?

---

### 🌳 Level 3: Advanced (Week 6-8)
**Goal**: Master advanced topics and specialization

**Topics to Cover:**
1. **Advanced Theory**
   - Complex aspects of {topic}
   - Optimization and performance considerations
   - Latest research and trends in {topic}

2. **Expert Skills**
   - Advanced patterns and architectures
   - Debugging and troubleshooting {topic}
   - Integration with other technologies

3. **Real-World Mastery**
   - Capstone project: Comprehensive application of {topic}
   - Contribution to open-source or community
   - Teaching others - best way to master

**Resources:**
- 📹 Videos: Advanced conference talks on {topic} (e.g., from Google I/O, academic conferences)
- 📄 Articles: Research papers on arXiv related to {topic}, advanced blogs
- 📚 Books: Advanced reference books, "Designing {topic} Systems"
- 💻 Practice: Build portfolio project, participate in competitions, contribute to GitHub

**Milestone Check:** Can you teach {topic} and solve complex problems?

---

### 🚀 Level 4: Expert & Beyond (Ongoing)
**Goal**: Stay updated and become thought leader

- Follow latest developments in {topic}
- Join communities: Discord, Slack, forums dedicated to {topic}
- Attend workshops and webinars
- Mentor beginners
- Explore related fields that complement {topic}

---

## 📅 Suggested Timeline

| Week | Focus | Hours/Week | Key Outcome |
|------|-------|------------|-------------|
| 1-2 | Beginner Fundamentals | 5-7 hrs | Clear basic understanding |
| 3-5 | Intermediate Practice | 7-10 hrs | Can build small projects |
| 6-8 | Advanced Mastery | 10-12 hrs | Portfolio-ready skills |
| 9+ | Expert Continuous | 3-5 hrs | Stay updated |

**Total Estimated Time**: 60-80 hours for proficiency

---

## 🛠️ Recommended Tools & Platforms

- **Learning**: YouTube, Coursera, edX, Khan Academy, Udemy
- **Practice**: LeetCode, HackerRank, Kaggle (if data-related), GitHub
- **Community**: Stack Overflow, Reddit, Discord communities
- **Documentation**: Official docs for {topic}
- **Projects**: Build in public, share on LinkedIn/GitHub

---

## 💡 Study Tips for {topic}

1. **Active Recall**: Test yourself regularly, don't just re-read
2. **Spaced Repetition**: Review concepts at increasing intervals
3. **Feynman Technique**: Explain {topic} in simple terms as if teaching a child
4. **Hands-On**: 70% practice, 30% theory
5. **Consistency**: 1 hour daily beats 7 hours on weekend

---

## 🎯 Success Metrics

- [ ] Can define {topic} and its importance
- [ ] Completed 3 beginner exercises
- [ ] Built 1 intermediate project
- [ ] Solved 5 real-world problems using {topic}
- [ ] Can explain advanced concepts to others
- [ ] Have portfolio project showcasing {topic}

---

## 🔗 Quick Resource Links (Template - Search these)

- YouTube: "https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+tutorial"
- Google: "https://www.google.com/search?q=learn+{topic.replace(' ', '+')}+roadmap"
- GitHub: "https://github.com/search?q={topic.replace(' ', '+')}"
- Coursera: Search for {topic} courses
- Articles: "https://medium.com/search?q={topic.replace(' ', '%20')}"

---

*💡 Pro Tip: Use EduGenie's other features to accelerate learning:*
- *Ask specific questions with QnA*
- *Get simplified explanations*
- *Generate quizzes to test understanding*
- *Summarize long articles on {topic}*

*Note: This is a fallback learning path. For truly personalized AI-generated path with specific video links, articles, books, and adaptive difficulty based on your level, configure GEMINI_API_KEY to use Gemini 1.5 Pro.*

Good luck with your learning journey in {topic}! 🌟
"""

def get_learning_recommendations(topic: str) -> Dict:
    """
    Generate personalized structured learning path for any given topic
    """
    if not topic or not topic.strip():
        return {"error": "Topic cannot be empty", "learning_path": None}
    
    topic = topic.strip()
    
    if len(topic) < 2:
        return {"error": "Topic too short", "learning_path": None}
    
    # Try Gemini
    if has_gemini_key():
        try:
            import google.generativeai as genai
            from .config import GEMINI_API_KEY
            
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(get_gemini_model_name())
            
            prompt = f"""You are EduGenie, an AI learning path designer.

Task: Generate a personalized, structured learning path for the topic "{topic}".

Requirements:
- Organize from beginner to advanced
- Include 3-4 levels: Beginner, Intermediate, Advanced, Expert
- For each level: topics to cover, estimated timeline, resources (videos, articles, books), hands-on projects, milestone checks
- Suggest specific, real resources where possible (e.g., YouTube channels, Coursera, books)
- Include timeline (weeks), hours per week, study tips, success metrics
- Make it adaptable to learner's level
- Use emojis and clear formatting for readability
- Be specific to "{topic}" - not generic
- Include practical, actionable steps
- Length: comprehensive but concise (400-600 words)

Topic: {topic}

Generate detailed learning path:"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return {
                    "learning_path": response.text.strip(),
                    "source": "gemini",
                    "model": get_gemini_model_name(),
                    "topic": topic
                }
            else:
                logger.warning("Gemini empty response for learning path")
                fallback = _fallback_learning_path(topic)
                return {
                    "learning_path": fallback,
                    "source": "fallback",
                    "model": "fallback",
                    "topic": topic,
                    "note": "Gemini empty response"
                }
                
        except Exception as e:
            logger.error(f"Gemini learning path error: {e}")
            fallback = _fallback_learning_path(topic)
            return {
                "learning_path": fallback,
                "source": "fallback",
                "model": "fallback",
                "topic": topic,
                "error_detail": str(e)
            }
    else:
        fallback = _fallback_learning_path(topic)
        return {
            "learning_path": fallback,
            "source": "fallback",
            "model": "fallback",
            "topic": topic,
            "note": "No API key, using fallback"
        }
