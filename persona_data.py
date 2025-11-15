"""Persona metadata used by the Friend Connection System."""

PERSONAS = {
    "Alice": {
        "id": "Alice",
        "full_name": "Alice Lin",
        "age": 22,
        "title": "The Super Connector",
        "summary": (
            "Alice Lin, 22, is an energetic university student recognized for her "
            "leadership in student organizations. She thrives on building "
            "relationships and facilitating collaboration across diverse social "
            "groups. Her charisma draws people together, though she often struggles "
            "to maintain deeper one-on-one connections."
        ),
        "personality_traits": ["Empathetic", "Organized", "Confident", "Outgoing"],
        "pain_points": [
            "Finds it hard to sustain meaningful friendships beyond initial introductions.",
            "Overwhelmed by managing too many social interactions.",
        ],
        "goals": [
            "Seeks tools to identify and strengthen valuable relationships.",
            "Aims to streamline her networking efforts for quality over quantity.",
        ],
        "technology": (
            "Highly active on LinkedIn, Discord, and event-management platforms. "
            "Frequently creates group chats and hosts online gatherings."
        ),
        "system_insight": (
            "Alice's behavior patterns can guide the system to recognize connector "
            "types who unify multiple social clusters."
        ),
    },
    "Bob": {
        "id": "Bob",
        "full_name": "Bob Chen",
        "age": 24,
        "title": "The Quiet Specialist",
        "summary": (
            "Bob Chen, 24, is a graduate research assistant known for his analytical "
            "mindset and calm demeanor. He values intellectual conversations over "
            "casual small talk and prefers structured, purpose-driven interactions."
        ),
        "personality_traits": ["Analytical", "Patient", "Reliable", "Introverted"],
        "pain_points": [
            "Finds it challenging to meet like-minded peers outside his research field.",
            "Feels disconnected from larger social circles.",
        ],
        "goals": [
            "Hopes to discover peers who share niche academic interests.",
            "Seeks meaningful, discussion-based friendships.",
        ],
        "technology": (
            "Primarily uses Slack, ResearchGate, and academic forums; less active on "
            "mainstream social media."
        ),
        "system_insight": (
            "Bob's data can train the system to match quieter, research-oriented "
            "users based on shared academic or professional interests."
        ),
    },
    "Charlie": {
        "id": "Charlie",
        "full_name": "Charlie Wang",
        "age": 21,
        "title": "The Event Butterfly",
        "summary": (
            "Charlie Wang, 21, is a marketing student and avid eventgoer. She loves "
            "meeting new people at social gatherings and thrives in energetic group "
            "settings. However, she often feels her relationships remain surface-level."
        ),
        "personality_traits": ["Sociable", "Enthusiastic", "Creative", "Expressive"],
        "pain_points": [
            "Struggles to build genuine, lasting friendships.",
            "Often feels lonely despite being socially active.",
        ],
        "goals": [
            "Wants to identify people who share her values beyond social appearances.",
            "Aims to transform event acquaintances into meaningful connections.",
        ],
        "technology": (
            "Highly active on Instagram, TikTok, and event apps like Meetup and "
            "Eventbrite."
        ),
        "system_insight": (
            "Charlie's profile helps the system detect users who appear socially "
            "active but require deeper compatibility matching."
        ),
    },
    "David": {
        "id": "David",
        "full_name": "David Liu",
        "age": 28,
        "title": "The Industry Insider",
        "summary": (
            "David Liu, 28, is a software engineer and university alumnus who mentors "
            "students entering the tech industry. He enjoys sharing real-world "
            "insights and connecting mentees to professional opportunities."
        ),
        "personality_traits": ["Experienced", "Strategic", "Supportive", "Professional"],
        "pain_points": [
            "Limited visibility into which students align with his interests.",
            "Time constraints for mentoring multiple mentees effectively.",
        ],
        "goals": [
            "Wants to identify motivated students for mentorship.",
            "Seeks efficient ways to network with potential collaborators or hires.",
        ],
        "technology": "Active on LinkedIn, GitHub, and university alumni platforms.",
        "system_insight": (
            "David's profile data can help the system match mentors with mentees "
            "based on skill compatibility and career trajectory."
        ),
    },
    "Emily": {
        "id": "Emily",
        "full_name": "Emily Chang",
        "age": 23,
        "title": "The Commuter Pragmatist",
        "summary": (
            "Emily Chang, 23, is a part-time student who balances work and study. She "
            "values efficiency in her social interactions and prefers relationships "
            "that align with her academic or professional goals."
        ),
        "personality_traits": ["Practical", "Reliable", "Independent", "Focused"],
        "pain_points": [
            "Limited time for campus engagement.",
            "Finds spontaneous meetups inconvenient due to schedule constraints.",
        ],
        "goals": [
            "Seeks dependable study partners and project collaborators.",
            "Prefers connections that fit into her structured schedule.",
        ],
        "technology": (
            "Uses productivity tools like Notion and Google Calendar; engages "
            "selectively on messaging apps."
        ),
        "system_insight": (
            "Emily's data can help optimize recommendations for users who prioritize "
            "efficiency and reliability in forming connections."
        ),
    },
    "Frank": {
        "id": "Frank",
        "full_name": "Frank",
        "age": 22,
        "title": "The Online DM Starter",
        "summary": (
            "Frank, 22, is a computer science student who prefers online interactions "
            "over face-to-face communication. He's expressive in text but reserved in "
            "person."
        ),
        "personality_traits": ["Introverted", "Thoughtful", "Tech-savvy", "Friendly"],
        "pain_points": [
            "Struggles to transition online chats into real-world friendships.",
            "Feels misunderstood due to quiet demeanor offline.",
        ],
        "goals": [
            "Aims to build confidence in in-person interactions.",
            "Wants to connect with peers who appreciate digital communication styles.",
        ],
        "technology": (
            "Active on Discord, Reddit, and coding communities; initiates "
            "conversations online."
        ),
        "system_insight": (
            "Frank's interactions inform the design of tools that bridge "
            "online-to-offline friendship development."
        ),
    },
    "Grace": {
        "id": "Grace",
        "full_name": "Grace",
        "age": 21,
        "title": "The Project Grinder",
        "summary": (
            "Grace, 21, is a hackathon enthusiast and creative developer who thrives "
            "in teamwork and innovation. She values commitment, technical skill, and "
            "collaboration."
        ),
        "personality_traits": ["Ambitious", "Hardworking", "Innovative", "Driven"],
        "pain_points": [
            "Frustrated when teammates lack discipline or follow-through.",
            "Finds it hard to connect with people who match her pace.",
        ],
        "goals": [
            "Seeks peers who share her work ethic and curiosity.",
            "Aims to form reliable teams for competitions and projects.",
        ],
        "technology": (
            "Uses GitHub, Notion, and hackathon platforms; collaborates through "
            "online project tools."
        ),
        "system_insight": (
            "Grace's collaboration habits can help refine matchmaking for "
            "skill-based and productivity-driven users."
        ),
    },
    "Henry": {
        "id": "Henry",
        "full_name": "Henry",
        "age": 27,
        "title": "The Gatekeeper",
        "summary": (
            "Henry, 27, manages a research lab and plays a key role in mentoring "
            "younger students. He's methodical, responsible, and values structure in "
            "relationships."
        ),
        "personality_traits": ["Disciplined", "Responsible", "Analytical", "Selective"],
        "pain_points": [
            "Finds it challenging to identify mentees with potential.",
            "Prefers meaningful over casual interactions.",
        ],
        "goals": [
            "Wants to mentor capable, goal-driven students.",
            "Aims to filter meaningful connections efficiently.",
        ],
        "technology": (
            "Uses LinkedIn, Trello, and lab management tools; prefers structured "
            "communication."
        ),
        "system_insight": (
            "Henry's mentorship data can help design visibility algorithms for "
            "mentors and institutional leaders."
        ),
    },
    "Ivan": {
        "id": "Ivan",
        "full_name": "Ivan",
        "age": 23,
        "title": "The International Bridge",
        "summary": (
            "Ivan, 23, is an exchange student passionate about cross-cultural "
            "experiences. He bridges communities through empathy and curiosity about "
            "diverse perspectives."
        ),
        "personality_traits": ["Open-minded", "Empathetic", "Curious", "Adaptable"],
        "pain_points": [
            "Faces cultural and language barriers in forming close friendships.",
            "Occasionally feels excluded from local groups.",
        ],
        "goals": [
            "Seeks genuine intercultural friendships.",
            "Aims to help international and local students connect.",
        ],
        "technology": "Active on WhatsApp, Telegram, and intercultural student forums.",
        "system_insight": (
            "Ivan's profile supports features that foster diversity-aware friend "
            "suggestions."
        ),
    },
    "Julia": {
        "id": "Julia",
        "full_name": "Julia",
        "age": 24,
        "title": "The Focused Closer",
        "summary": (
            "Julia, 24, is a business analyst who values purpose-driven networking. "
            "She approaches relationships strategically, preferring mentorship and "
            "professional growth over casual chats."
        ),
        "personality_traits": ["Goal-oriented", "Strategic", "Assertive", "Professional"],
        "pain_points": [
            "Feels small talk wastes time.",
            "Finds it hard to identify mentors who align with her vision.",
        ],
        "goals": [
            "Aims to build connections that accelerate her career growth.",
            "Seeks mentorship from experienced professionals.",
        ],
        "technology": "Primarily active on LinkedIn, Notion, and productivity apps.",
        "system_insight": (
            "Julia's usage patterns can enhance professional matching and mentorship "
            "features within the system."
        ),
    },
    "Kevin": {
        "id": "Kevin",
        "full_name": "Kevin",
        "age": 20,
        "title": "The Study Buddy",
        "summary": (
            "Kevin, 20, is a dependable undergraduate student who values teamwork and "
            "collaboration in academic settings."
        ),
        "personality_traits": ["Cooperative", "Responsible", "Friendly", "Supportive"],
        "pain_points": [
            "Struggles to find consistent study partners.",
            "Dislikes competitive or overly casual learning groups.",
        ],
        "goals": [
            "Seeks reliable peers for long-term academic support.",
            "Aims to improve group learning through structured study sessions.",
        ],
        "technology": "Uses Google Docs, Discord, and study planner apps.",
        "system_insight": (
            "Kevin's consistent behavior patterns can improve academic-group "
            "formation algorithms."
        ),
    },
    "Laura": {
        "id": "Laura",
        "full_name": "Laura",
        "age": 29,
        "title": "The Alumni Connector",
        "summary": (
            "Laura, 29, is a university graduate who maintains strong ties with her "
            "alma mater. She values giving back to students through advice and "
            "networking."
        ),
        "personality_traits": ["Friendly", "Professional", "Supportive", "Loyal"],
        "pain_points": [
            "Limited opportunities to engage with current students.",
            "Finds it hard to identify mentees genuinely interested in alumni insights.",
        ],
        "goals": [
            "Wants to bridge alumni and student communities.",
            "Aims to maintain a sense of belonging to her university.",
        ],
        "technology": "Active on alumni networks, LinkedIn, and university event pages.",
        "system_insight": (
            "Laura's participation data can improve alumni-student network engagement "
            "analytics."
        ),
    },
    "Mike": {
        "id": "Mike",
        "full_name": "Mike",
        "age": 22,
        "title": "The Idea Inventor",
        "summary": (
            "Mike, 22, is a creative designer with a passion for innovation. He "
            "thrives in brainstorming sessions and multidisciplinary teamwork."
        ),
        "personality_traits": ["Innovative", "Curious", "Expressive", "Visionary"],
        "pain_points": [
            "Finds it hard to find equally creative collaborators.",
            "Often feels misunderstood by more pragmatic peers.",
        ],
        "goals": [
            "Seeks creative partners to build original projects.",
            "Aims to turn abstract ideas into concrete outcomes.",
        ],
        "technology": (
            "Active on Figma, Behance, and creative Discord servers."
        ),
        "system_insight": (
            "Mike's profile can inform algorithms for pairing innovation-oriented "
            "users across disciplines."
        ),
    },
    "Nancy": {
        "id": "Nancy",
        "full_name": "Nancy",
        "age": 20,
        "title": "The Anxious Introvert",
        "summary": (
            "Nancy, 20, is a shy and reflective freshman who often struggles to "
            "initiate social interactions. She values kindness and prefers deep, "
            "slow-growing friendships."
        ),
        "personality_traits": ["Gentle", "Thoughtful", "Reserved", "Empathetic"],
        "pain_points": [
            "Experiences anxiety in group settings.",
            "Feels invisible in large social environments.",
        ],
        "goals": [
            "Hopes to meet friends who understand her quiet personality.",
            "Wants to build confidence in social engagement.",
        ],
        "technology": (
            "Uses journaling apps, low-pressure messaging platforms, and small online "
            "communities."
        ),
        "system_insight": (
            "Nancy's journey can guide inclusive design for shy or socially anxious "
            "users."
        ),
    },
    "Oliver": {
        "id": "Oliver",
        "full_name": "Oliver",
        "age": 25,
        "title": "The Helpful Listener",
        "summary": (
            "Oliver, 25, is a counseling assistant known for his empathy and "
            "patience. He often serves as an emotional support resource for peers, "
            "helping others feel heard and understood."
        ),
        "personality_traits": ["Empathetic", "Patient", "Supportive", "Calm"],
        "pain_points": [
            "Emotionally drained from constantly supporting others.",
            "Struggles to find reciprocal friendships.",
        ],
        "goals": [
            "Hopes to build balanced relationships with mutual support.",
            "Wants to use his listening skills to strengthen community well-being.",
        ],
        "technology": (
            "Uses messaging platforms for check-ins; participates in mental wellness "
            "forums."
        ),
        "system_insight": (
            "Oliver's empathy-driven data can guide features promoting emotional "
            "well-being in friendship systems."
        ),
    },
    "Peter": {
        "id": "Peter",
        "full_name": "Peter",
        "age": 26,
        "title": "The Ambitious Leader",
        "summary": (
            "Peter, 26, is a startup founder driven by vision and leadership. He's "
            "charismatic, persuasive, and thrives on collaboration toward ambitious "
            "goals."
        ),
        "personality_traits": ["Charismatic", "Visionary", "Determined", "Confident"],
        "pain_points": [
            "Struggles to find equally motivated collaborators.",
            "Balances between leadership and personal connection.",
        ],
        "goals": [
            "Seeks to recruit cofounders or motivated peers.",
            "Aims to mentor and inspire entrepreneurial students.",
        ],
        "technology": "Active on LinkedIn, Twitter (X), and startup communities.",
        "system_insight": (
            "Peter's data can train matching algorithms for leadership-driven "
            "community building."
        ),
    },
    "Quinn": {
        "id": "Quinn",
        "full_name": "Quinn",
        "age": 21,
        "title": "The Gamer Friend",
        "summary": (
            "Quinn, 21, is a streamer and gamer who values humor and relaxed "
            "companionship. He finds connection through shared play and late-night "
            "chats."
        ),
        "personality_traits": ["Playful", "Friendly", "Laid-back", "Loyal"],
        "pain_points": [
            "Struggles to maintain consistent communication outside gaming.",
            "Finds it hard to connect with non-gamers.",
        ],
        "goals": [
            "Hopes to find regular gaming friends and social circles.",
            "Wants friendships that extend beyond online play.",
        ],
        "technology": "Uses Discord, Twitch, and gaming voice channels daily.",
        "system_insight": (
            "Quinn's behavior helps improve virtual friendship matching through "
            "shared recreational interests."
        ),
    },
    "Rachel": {
        "id": "Rachel",
        "full_name": "Rachel",
        "age": 27,
        "title": "The Mentor Coach",
        "summary": (
            "Rachel, 27, is a teaching assistant passionate about helping students "
            "grow personally and academically. She balances professionalism with "
            "warmth."
        ),
        "personality_traits": ["Supportive", "Encouraging", "Responsible", "Compassionate"],
        "pain_points": [
            "Finds it difficult to track the long-term growth of students.",
            "Occasionally overextends herself to help others.",
        ],
        "goals": [
            "Seeks to empower students through continuous mentorship.",
            "Aims to connect with learners beyond the classroom.",
        ],
        "technology": (
            "Active on educational platforms, mentorship networks, and messaging "
            "tools for student feedback."
        ),
        "system_insight": (
            "Rachel's mentorship data can guide the system to support coaching and "
            "guidance-driven connections."
        ),
    },
    "Sam": {
        "id": "Sam",
        "full_name": "Sam",
        "age": 23,
        "title": "The Event Planner",
        "summary": (
            "Sam, 23, is an event organizer who thrives on creating social "
            "opportunities for others. She's approachable, detail-oriented, and "
            "data-minded."
        ),
        "personality_traits": ["Organized", "Outgoing", "Creative", "Efficient"],
        "pain_points": [
            "Overwhelmed by coordination logistics.",
            "Finds it hard to measure event success beyond attendance.",
        ],
        "goals": [
            "Wants to design events that encourage lasting friendships.",
            "Seeks data insights to improve community engagement.",
        ],
        "technology": (
            "Uses Notion, Google Sheets, and social event software like Eventbrite."
        ),
        "system_insight": (
            "Sam's behavioral data can support the system's community analytics for "
            "engagement tracking."
        ),
    },
    "Tom": {
        "id": "Tom",
        "full_name": "Tom",
        "age": 22,
        "title": "The Club Recruiter",
        "summary": (
            "Tom, 22, is a student organization recruiter passionate about "
            "discovering talented new members. He's persuasive, goal-driven, and "
            "enjoys networking."
        ),
        "personality_traits": ["Energetic", "Strategic", "Charismatic", "Outgoing"],
        "pain_points": [
            "Hard to find candidates who align with club values.",
            "Balances quantity of recruits with quality.",
        ],
        "goals": [
            "Wants to identify potential leaders efficiently.",
            "Aims to expand club diversity while maintaining cohesion.",
        ],
        "technology": "Uses social media, club management tools, and university forums.",
        "system_insight": (
            "Tom's recruitment data helps optimize member recommendation algorithms "
            "for student groups."
        ),
    },
    "Uma": {
        "id": "Uma",
        "full_name": "Uma",
        "age": 22,
        "title": "The Super Connector",
        "summary": (
            "Uma, 22, is a university student who mirrors Alice's connector "
            "personality - enthusiastic, socially driven, and naturally inclusive. "
            "She builds bridges between isolated classmates."
        ),
        "personality_traits": ["Friendly", "Energetic", "Empathetic", "Organized"],
        "pain_points": [
            "Struggles to balance breadth and depth in friendships.",
            "Spends too much time maintaining social connections.",
        ],
        "goals": [
            "Hopes to manage her network more effectively.",
            "Wants to ensure no one feels left out.",
        ],
        "technology": (
            "Active in student organizations, Discord groups, and event chats."
        ),
        "system_insight": (
            "Uma's profile reinforces social mapping tools that visualize and connect "
            "fragmented communities."
        ),
    },
    "Victor": {
        "id": "Victor",
        "full_name": "Victor",
        "age": 28,
        "title": "The Industry Insider",
        "summary": (
            "Victor, 28, is a seasoned software engineer and university alumnus who "
            "values mentoring and career guidance."
        ),
        "personality_traits": ["Professional", "Insightful", "Helpful", "Strategic"],
        "pain_points": [
            "Time constraints limit his ability to engage with mentees.",
            "Finds it hard to discover mentees with genuine initiative.",
        ],
        "goals": [
            "Seeks to mentor students aligned with his field.",
            "Aims to build a professional support network.",
        ],
        "technology": "Uses LinkedIn, GitHub, and professional alumni channels.",
        "system_insight": (
            "Victor's engagement patterns enhance mentor discovery and "
            "industry-academia integration."
        ),
    },
}


def get_persona(name):
    """Return persona data for a given name if it exists."""
    if not name:
        return None
    return PERSONAS.get(name)
