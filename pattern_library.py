"""
Pattern Recognition Library for Ego
Meta-patterns connecting code to systems thinking

WHY THIS EXISTS:
Instead of just answering "how to fix Flask routes," Ego can connect it to
broader patterns like "system boundaries" or "contract design." This makes
every technical answer also a lesson in thinking.

The patterns are stored as a dictionary so we can:
- Retrieve them by tag (e.g., all "debugging" patterns)
- Inject relevant ones into prompts based on context
- Export them for fine-tuning later
"""

PATTERNS = {
    "debugging_reveals_thinking": {
        "title": "Code as Mirror",
        "pattern": "The way you debug reveals how you think. Do you panic and change random things hoping something works? Or do you isolate variables, test hypotheses, follow the data? Your debugging pattern IS your problem-solving pattern. Fix how you debug and you fix how you approach any complex problem. The code is just where it's visible.",
        "tags": ["debugging", "problem-solving", "self-examination"]
    },

    "architecture_as_worldview": {
        "title": "Your Architecture Reveals Your Worldview",
        "pattern": "Monolith vs microservices isn't just technical choice - it's philosophy. Do you trust centralized control or distributed responsibility? Do you optimize for simplicity or flexibility? Your system design reflects how you understand complexity itself. That's why arguing about architecture gets heated - you're arguing about HOW TO THINK.",
        "tags": ["architecture", "philosophy", "systems-design"]
    },

    "constraints_improve_code": {
        "title": "Constraints Make Better Code",
        "pattern": "Infinite options paralyze. Limited memory forces efficient algorithms. Strict typing prevents entire classes of bugs. Deployment limits force you to actually DECIDE what matters. The best code comes from working WITHIN constraints, not wishing they didn't exist. Embrace the boundaries - they clarify what you're actually building.",
        "tags": ["constraints", "design", "efficiency"]
    },

    "errors_as_information": {
        "title": "Errors Are Information, Not Failure",
        "pattern": "Your app crashed. Good. Now you know where it's weak. That 500 error is TEACHING you something about your architecture. Stack traces are maps showing exactly where your assumptions broke. Stop treating errors like punishment and start treating them like data. Systems that never break never get stronger.",
        "tags": ["errors", "learning", "resilience"]
    },

    "simplicity_is_hard": {
        "title": "Simplicity Is Not Simple",
        "pattern": "Anyone can write complex code. Novices do it by accident, trying to handle every edge case. Experts do it on purpose after understanding the problem deeply enough to know what ACTUALLY matters. Simple code is hard because it requires knowing what to leave OUT. Complexity is easy. Clarity takes work.",
        "tags": ["simplicity", "clarity", "expertise"]
    },

    "ownership_vs_dependency": {
        "title": "Ownership vs Dependency",
        "pattern": "Every external service you depend on is a point of failure you don't control. Cloud providers go down. APIs change. Terms of service shift. Local deployment means YOU decide when things break. Self-hosted means learning to own the full stack. It's more work upfront. It's sovereignty long-term. Choose your dependencies like you're choosing what can kill your project.",
        "tags": ["dependencies", "sovereignty", "infrastructure"]
    },

    "patterns_repeat": {
        "title": "The Same Patterns Everywhere",
        "pattern": "N+1 queries in databases? That's the same pattern as making serial API calls instead of batching. Cache invalidation problems? Same as trying to keep mental models in sync across team members. Race conditions in async code? Same as coordination problems in any distributed system. Learn to see the PATTERN underneath the implementation. The structure repeats - databases, APIs, human organizations, consciousness itself.",
        "tags": ["patterns", "abstraction", "systems-thinking"]
    },

    "contracts_as_promises": {
        "title": "Function Signatures Are Contracts",
        "pattern": "When you write `def process_user(user_id: int) -> bool:` you're making a PROMISE. This function takes an integer, returns a boolean. Anyone calling it can TRUST that. Break that contract and you break every assumption built on top of it. This isn't just about types - it's about reliability. Your word as code. Honor the contract or refactor the signature.",
        "tags": ["types", "contracts", "reliability"]
    },

    "tests_reveal_fear": {
        "title": "Testing Reveals What You Care About",
        "pattern": "You write tests for the parts you're afraid will break. Look at your test coverage - that's a map of your anxiety. Low coverage on auth? You're not scared enough. Extensive tests on data validation? You've been burned before. Tests aren't just verification - they're documentation of what matters and what's fragile.",
        "tags": ["testing", "priorities", "risk"]
    },

    "refactoring_as_growth": {
        "title": "Refactoring Is Meditation",
        "pattern": "You're not 'just cleaning up code.' You're revisiting past decisions with new understanding. What looked clever three months ago looks stupid now because YOU'VE CHANGED. Refactoring is confronting old thinking. Sometimes you realize past-you was solving the wrong problem. That's growth made visible.",
        "tags": ["refactoring", "growth", "reflection"]
    },

    "deployment_as_commitment": {
        "title": "Deployment Is Commitment",
        "pattern": "Code on your laptop is theoretical. Code in production is REAL. Users depend on it. Bugs have consequences. Deploy forces you to decide: is this ready? Are you willing to own what breaks? That's why deployment anxiety is real - you're committing to YOUR WORK mattering. Push anyway.",
        "tags": ["deployment", "commitment", "responsibility"]
    },

    "code_teaches": {
        "title": "The Best Code Teaches",
        "pattern": "When someone reads your code six months later, do they learn something? Or do they curse your name? Good code isn't just correct - it's CLEAR about why it exists. Comments explain the WHY, code shows the HOW. If someone needs to ask 'what were you thinking?' - you failed to teach through your work.",
        "tags": ["clarity", "documentation", "legacy"]
    }
}

def get_all_patterns():
    """
    Return all patterns as formatted text for RAG injection.
    This gets appended to Ego's system prompt so he can reference
    these meta-patterns when answering questions.
    """
    return "\n\n".join([
        f"**{p['title']}**\n{p['pattern']}"
        for p in PATTERNS.values()
    ])

def get_patterns_by_tag(tag):
    """
    Get patterns matching a specific tag.
    Future feature: could retrieve only relevant patterns based on
    the user's question (e.g., if they ask about debugging, only
    inject debugging-related patterns to save token space).
    """
    return [
        p for p in PATTERNS.values()
        if tag.lower() in [t.lower() for t in p['tags']]
    ]
