#!/usr/bin/env python3
"""
Exam Question Raffle System
Organize and practice exam questions by topic
"""

import random
import json
from collections import defaultdict

# Question database with categorization
QUESTIONS = {
    "Exam 1": {
        "Q1": {
            "text": "Consider f(x,y)=|(x,y)|-x=√(x²+y²)-x. Find its extreme points in the region |(x,y)|≤2. Also classify other points of interest.",
            "topics": ["Extrema/Optimization", "Constrained Optimization"]
        },
        "Q2": {
            "text": "A mountain has the shape f(x,y)=(x+sin y)cos(πx²+y). You are at (2,0).\na) In which direction is the steepest slope (upwards).\nb) What is the slope in this direction.\nc) Maximum inclination you can handle is 45°. In which direction to move?",
            "topics": ["Gradient", "Directional Derivatives", "Steepest Ascent/Descent"]
        },
        "Q3a": {
            "text": "Write a formula for the tangent plane at the point (2,0) for f from Problem 2.",
            "topics": ["Tangent Plane"]
        },
        "Q3b": {
            "text": "Write a formula for the second order Taylor approximation at (2,0) for f from Problem 2.",
            "topics": ["Taylor Approximation"]
        },
        "Q3c": {
            "text": "Consider integral ∬g(u,v)dudv and change of variables u=f(x,y), v=xy. What is the Jacobian at (2,0)?",
            "topics": ["Jacobian", "Change of Variables"]
        },
        "Q4": {
            "text": "Compute, as far as possible, the derivative of f(r)=∫₀ʳ e^(-rx²)dx. Justify your computations.",
            "topics": ["Differentiation of Integrals", "Leibniz Rule"]
        },
        "Q5": {
            "text": "Body B: 0≤x≤cos y where -π/2≤y≤π/2, and |z|≤x². Compute ∭_B sin y dx dy dz",
            "topics": ["Triple Integrals", "Volume"]
        },
        "Q6": {
            "text": "Compute ∬_ℝ² e^(-x²-y²) using polar coordinates. Then find ∫_ℝ e^(-x²)dx.",
            "topics": ["Polar Coordinates", "Double Integrals", "Gaussian Integral"]
        }
    },
    "Exam 2": {
        "Q1a": {
            "text": "Explain the difference between f having two partial derivatives at (x₀,y₀), and being differentiable at (x₀,y₀).",
            "topics": ["Partial Derivatives", "Differentiability", "Theory"]
        },
        "Q1b": {
            "text": "If f is C² and there exists C² function g such that ∂f/∂x=∂g/∂y and ∂f/∂y=-∂g/∂x, show f fulfills ∂²f/∂x²+∂²f/∂y²=0",
            "topics": ["Partial Differential Equations", "Laplace Equation", "Theory"]
        },
        "Q1c": {
            "text": "Show that f(x,y)=arctan(y/x) satisfies the Laplace equation off the x-axis.",
            "topics": ["Partial Differential Equations", "Laplace Equation"]
        },
        "Q2a": {
            "text": "Find the equation for the tangent plane of f(x,y)=arctan(y/x) at (2,2).",
            "topics": ["Tangent Plane"]
        },
        "Q2b": {
            "text": "What is the normal vector to the plane in Q2a?",
            "topics": ["Normal Vector", "Tangent Plane"]
        },
        "Q2c": {
            "text": "At point (1,-1,2), in what direction is f(x,y,z)=x/||(x,y,z)|| increasing the most?",
            "topics": ["Gradient", "Directional Derivatives"]
        },
        "Q3": {
            "text": "Consider f(x,y)=3x²-4xy+y². Show origin is a critical point and determine if it's local max, min or saddle point.",
            "topics": ["Critical Points", "Hessian", "Second Derivative Test"]
        },
        "Q4a": {
            "text": "∬_D x dA where D={(x,y): 1≤x≤2, x²≤y≤x³}. Sketch the region.",
            "topics": ["Double Integrals", "Integration Regions"]
        },
        "Q4b": {
            "text": "∬_D 1/(x+y) dA where D={(x,y): 1≤y≤2, 0≤x≤y}. Sketch the region.",
            "topics": ["Double Integrals", "Integration Regions"]
        },
        "Q4c": {
            "text": "∬_D e^(x²+y²) dA where D={(x,y): x²+y²≤2}. Sketch the region.",
            "topics": ["Double Integrals", "Polar Coordinates"]
        },
        "Q5": {
            "text": "Show x+y+z+cos(xyz)=0 locally defines z as function φ of (x,y) near (0,0,-1). Compute ∂φ/∂x(0,0) and ∂φ/∂y(0,0).",
            "topics": ["Implicit Function Theorem", "Implicit Differentiation"]
        },
        "Q6a": {
            "text": "Find max and min of f(x,y)=xy/√(1-x²-y²) in the unit disc.",
            "topics": ["Extrema/Optimization", "Constrained Optimization"]
        },
        "Q6b": {
            "text": "Find max and min of f(x,y)=x³y²(1-x-y) in first quadrant {(x,y): x≥0, y≥0}.",
            "topics": ["Extrema/Optimization", "Constrained Optimization"]
        }
    },
    "Exam 3": {
        "Q1a": {
            "text": "Explain where the factor r comes from when changing to polar coordinates in ℝ². Give intuitive explanation why angle θ doesn't appear.",
            "topics": ["Polar Coordinates", "Jacobian", "Theory"]
        },
        "Q1b": {
            "text": "Compute ∬_E arctan(√(x²+y²))dA where E={(x,y): 1≤x²+y²≤3, x/√3≤y≤√3x}.",
            "topics": ["Double Integrals", "Polar Coordinates"]
        },
        "Q2a": {
            "text": "Cinnamon bun flies along (t,t²,⅔t³) starting at t=0. What is speed and velocity at t=t₀?",
            "topics": ["Parametric Curves", "Velocity", "Speed"]
        },
        "Q2b": {
            "text": "At t=1 the bun runs out of fuel and continues along straight line with constant speed. Formula for trajectory for t>1?",
            "topics": ["Parametric Curves", "Tangent Lines"]
        },
        "Q2c": {
            "text": "What is the distance traveled between t=0 and t=1 (along the path)?",
            "topics": ["Arc Length", "Parametric Curves"]
        },
        "Q3a": {
            "text": "If ∇f(1,1,1)=(5,2,1) and x(t)=(t²,t⁻³,t), find d/dt f(x(t)) at t=1.",
            "topics": ["Chain Rule", "Gradient"]
        },
        "Q3b": {
            "text": "Find tangent plane to g(x,y)=x/√(x²+y²) at P=(3,-4,3/5).",
            "topics": ["Tangent Plane"]
        },
        "Q3c": {
            "text": "What is the normal line through P?",
            "topics": ["Normal Line", "Tangent Plane"]
        },
        "Q4a": {
            "text": "Change of variables s=2x³+3y², t=x. Is this really a change of variables (bijection)?",
            "topics": ["Change of Variables", "Jacobian", "Theory"]
        },
        "Q4b": {
            "text": "Show it's a bijection from half plane y>0 into a set in (s,t)-plane. Draw this set.",
            "topics": ["Change of Variables", "Theory"]
        },
        "Q4c": {
            "text": "Solve y∂u/∂x=x²∂u/∂y for y>0 using the change of variables.",
            "topics": ["Partial Differential Equations", "Change of Variables"]
        },
        "Q5": {
            "text": "Find surface area of cone of height h obtained by rotating z=3x around z-axis in ℝ³.",
            "topics": ["Surface Area", "Revolution Surfaces"]
        },
        "Q6a": {
            "text": "Find max and min of f(x,y)=(x²+2y²)e^(-x²+y²) in the unit disc.",
            "topics": ["Extrema/Optimization", "Constrained Optimization"]
        },
        "Q6b": {
            "text": "Find max and min of f(x,y)=(x²+2y²)e^(-x²+y²) in the plane ℝ².",
            "topics": ["Extrema/Optimization", "Unconstrained Optimization"]
        },
        "Q7": {
            "text": "For which α∈ℝ do we have lim_{(x,y)→0} x|y|^α/(x²+y⁴)=0? Hint: 2ab≤a²+b².",
            "topics": ["Limits", "Multivariable Limits"]
        }
    },
    "Exam 4": {
        "Q1a": {
            "text": "Body between z=cos r and z=sin r including point (0,0,1/2), where r=√(x²+y²). Draw it.",
            "topics": ["Volume", "Visualization"]
        },
        "Q1b": {
            "text": "Compute volume by first integrating in z then in (x,y).",
            "topics": ["Triple Integrals", "Volume", "Order of Integration"]
        },
        "Q1c": {
            "text": "Write formula for computing volume using slice method (reversing order).",
            "topics": ["Triple Integrals", "Volume", "Order of Integration"]
        },
        "Q2a": {
            "text": "For f(x,y)=e^(5-x²-y²), which is direction of maximum decrease at (2,1)?",
            "topics": ["Gradient", "Directional Derivatives", "Steepest Ascent/Descent"]
        },
        "Q2b": {
            "text": "Write formula for tangent plane at point (2,1).",
            "topics": ["Tangent Plane"]
        },
        "Q2c": {
            "text": "What is the Hessian for f at (2,1)?",
            "topics": ["Hessian", "Second Derivatives"]
        },
        "Q2d": {
            "text": "Write formula for second order Taylor approximation at (2,1).",
            "topics": ["Taylor Approximation"]
        },
        "Q3": {
            "text": "Compute area of piece of surface z=1+y² which lies above set |x|≤y≤1.",
            "topics": ["Surface Area"]
        },
        "Q4a": {
            "text": "For e^x+xy+e^y-2=u, x³-x+y+y³=v, show x,y can be written as C¹-functions of u,v near (0,0).",
            "topics": ["Implicit Function Theorem", "Jacobian"]
        },
        "Q4b": {
            "text": "Compute ∂_u x, ∂_v x, ∂_u y and ∂_v y at (0,0).",
            "topics": ["Implicit Function Theorem", "Implicit Differentiation"]
        },
        "Q4c": {
            "text": "Show that in small neighborhood of (0,0) there is no other solution to the system.",
            "topics": ["Implicit Function Theorem", "Theory"]
        },
        "Q5a": {
            "text": "For F(x,y)=xy(x-y)/(x²+y²) if (x,y)≠(0,0), 0 otherwise. Show F is not continuous at (0,0).",
            "topics": ["Continuity", "Limits"]
        },
        "Q5b": {
            "text": "Compute F₁(x,y) and F₂(x,y) for all (x,y).",
            "topics": ["Partial Derivatives"]
        },
        "Q5c": {
            "text": "Compute F₁₂(0,0) and F₂₁(0,0).",
            "topics": ["Mixed Partial Derivatives", "Second Derivatives"]
        },
        "Q5d": {
            "text": "Why isn't F₁₂(0,0)=F₂₁(0,0)?",
            "topics": ["Mixed Partial Derivatives", "Theory"]
        },
        "Q6a": {
            "text": "For f(x₁,x₂)=¼(|x₁|+|x₂|)²-¼(x₁²+x₂²), find critical and singular points.",
            "topics": ["Critical Points", "Singular Points", "Non-smooth Optimization"]
        },
        "Q6b": {
            "text": "Find the global minimum.",
            "topics": ["Extrema/Optimization", "Global Optimization"]
        },
        "Q6c": {
            "text": "Compute proximal operator prox_f(1,2) which minimizes f(x)+½||x-y||².",
            "topics": ["Extrema/Optimization", "Proximal Operators"]
        }
    },
    "Exam 5": {
        "Q1": {
            "text": "Compute volume of solid between cone z=4-√(x²+y²) and paraboloid z=x²+y²+2.",
            "topics": ["Triple Integrals", "Volume", "Polar Coordinates"]
        },
        "Q2a": {
            "text": "For cos(z)+x³+¼y⁴-y=1, what is tangent plane to level surface at (1,0,π/2)?",
            "topics": ["Tangent Plane", "Level Surfaces"]
        },
        "Q2b": {
            "text": "Around which points can solutions be expressed as (x,y(x,z),z) and (x(y,z),y,z)?",
            "topics": ["Implicit Function Theorem", "Level Surfaces"]
        },
        "Q3a": {
            "text": "Find extreme values of f(x,y)=x²+y²+sin(x²)+cos(y²) over region x²+y²≤π.",
            "topics": ["Extrema/Optimization", "Constrained Optimization"]
        },
        "Q3b": {
            "text": "What properties of D and f guarantee existence of max and min? Why do f and D in 3a satisfy this?",
            "topics": ["Extrema/Optimization", "Theory", "Extreme Value Theorem"]
        },
        "Q4a": {
            "text": "Transform PDE y∂u/∂x-x∂u/∂y=x+y using x=r cos(θ), y=r sin(θ).",
            "topics": ["Partial Differential Equations", "Change of Variables", "Polar Coordinates"]
        },
        "Q4b": {
            "text": "Solve this partial differential equation.",
            "topics": ["Partial Differential Equations"]
        },
        "Q5a": {
            "text": "Why can improper integral I be split into sum of four integrals?",
            "topics": ["Double Integrals", "Improper Integrals", "Theory"]
        },
        "Q5b": {
            "text": "Determine convergence of I=∬_D(x¹⁰y⁹-y sin(xy⁹)+x²+1/√(1-x²-y²))dA. If convergent, compute.",
            "topics": ["Double Integrals", "Improper Integrals", "Symmetry"]
        },
        "Q6a": {
            "text": "Compute F'(x) if F(x)=∫₀ˣ(x-y)f(y)dy.",
            "topics": ["Differentiation of Integrals", "Leibniz Rule"]
        },
        "Q6b": {
            "text": "What condition on f permits differentiation inside the integral?",
            "topics": ["Differentiation of Integrals", "Theory"]
        },
        "Q6c": {
            "text": "Let F_n(x)=∫₀ˣ(x-y)^(n-1)/(n-1)!·f(y)dy. Compute F_n^(n), the n'th derivative.",
            "topics": ["Differentiation of Integrals", "Leibniz Rule"]
        }
    },
    "Exam 6": {
        "Q1": {
            "text": "Compute 2nd degree Taylor polynomial at 0 for f(x,y)=2x+y+2cos(x+2y), then approximate f(0.1,0.2).",
            "topics": ["Taylor Approximation"]
        },
        "Q2a": {
            "text": "Person walks on road on hill f(x,y)=30-(x+2)²-y². Projection is unit circle. Find points of steepest ascent/descent and steepness.",
            "topics": ["Gradient", "Steepest Ascent/Descent", "Constrained Optimization"]
        },
        "Q2b": {
            "text": "At point (1,0,21), person heads north-east. What is slope in this direction?",
            "topics": ["Directional Derivatives"]
        },
        "Q3": {
            "text": "Infinite egg carton z=5cos(x+y)+3sin(2(x-y)). Determine all critical points and classify them.",
            "topics": ["Critical Points", "Hessian", "Second Derivative Test"]
        },
        "Q4a": {
            "text": "Compute ∬_D (x-2y)/(x²+y²)² dx dy where D is x≥1, y≥1.",
            "topics": ["Double Integrals", "Improper Integrals"]
        },
        "Q4b": {
            "text": "Compute ∬_D (x-2y)/(x²+y²)² dx dy where D is |(x,y)|≥2.",
            "topics": ["Double Integrals", "Improper Integrals", "Polar Coordinates"]
        },
        "Q5a": {
            "text": "Compute length of curve r(t)=(t³,t²,3t⁴) for 0≤t≤1.",
            "topics": ["Arc Length", "Parametric Curves"]
        },
        "Q5b": {
            "text": "Compute area of surface z=2√(1-x²-y²) above unit disc.",
            "topics": ["Surface Area"]
        },
        "Q6a": {
            "text": "For surface S: 2x+y³=3yz, for which points does defining z as function of x,y fail?",
            "topics": ["Implicit Function Theorem", "Level Surfaces"]
        },
        "Q6b": {
            "text": "For which points can you not solve for y as function of x,z?",
            "topics": ["Implicit Function Theorem", "Level Surfaces"]
        },
        "Q6c": {
            "text": "Show answer to 6b is parametrized by r(t)=(t³,t,t²). Show this curve lies in S.",
            "topics": ["Implicit Function Theorem", "Parametric Curves"]
        }
    }
}

# Create topic index
def build_topic_index():
    """Build an index mapping topics to questions."""
    topic_index = defaultdict(list)
    for exam, questions in QUESTIONS.items():
        for q_id, q_data in questions.items():
            for topic in q_data["topics"]:
                topic_index[topic].append({
                    "exam": exam,
                    "question_id": q_id,
                    "text": q_data["text"]
                })
    return dict(topic_index)

def display_topics():
    """Display all available topics."""
    topic_index = build_topic_index()
    topics = sorted(topic_index.keys())

    print("\n" + "="*70)
    print("AVAILABLE TOPICS")
    print("="*70)
    for i, topic in enumerate(topics, 1):
        count = len(topic_index[topic])
        print(f"{i:2d}. {topic:40s} ({count} questions)")
    print("="*70)
    return topics, topic_index

def get_random_question_by_topic(topic, topic_index, used_questions=None):
    """Get a random question from a specific topic."""
    if used_questions is None:
        used_questions = set()

    available = [q for q in topic_index[topic]
                 if (q["exam"], q["question_id"]) not in used_questions]

    if not available:
        return None

    return random.choice(available)

def display_question(question_data):
    """Display a question in a nice format."""
    print("\n" + "="*70)
    print(f"📚 {question_data['exam']} - {question_data['question_id']}")
    print("="*70)
    print(question_data['text'])
    print("="*70 + "\n")

def raffle_mode():
    """Interactive raffle mode."""
    print("\n" + "🎲"*35)
    print("       EXAM QUESTION RAFFLE - PRACTICE MODE")
    print("🎲"*35 + "\n")

    topics, topic_index = display_topics()
    used_questions = set()

    while True:
        print("\nOptions:")
        print("  [1-{}] - Select topic by number".format(len(topics)))
        print("  [r] - Random topic")
        print("  [s] - Show topics again")
        print("  [t] - Show topic statistics")
        print("  [reset] - Reset used questions")
        print("  [q] - Quit")

        choice = input("\nYour choice: ").strip().lower()

        if choice == 'q':
            print("\n✅ Good luck with your studies!\n")
            break
        elif choice == 's':
            topics, topic_index = display_topics()
        elif choice == 'r':
            topic = random.choice(topics)
            print(f"\n🎲 Random topic selected: {topic}")
            question = get_random_question_by_topic(topic, topic_index, used_questions)
            if question:
                display_question(question)
                used_questions.add((question['exam'], question['question_id']))
            else:
                print(f"❌ No more unused questions in topic: {topic}")
        elif choice == 't':
            show_statistics(topic_index, used_questions)
        elif choice == 'reset':
            used_questions.clear()
            print("\n✅ All questions reset! You can practice them again.\n")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(topics):
                topic = topics[idx]
                question = get_random_question_by_topic(topic, topic_index, used_questions)
                if question:
                    display_question(question)
                    used_questions.add((question['exam'], question['question_id']))
                else:
                    print(f"❌ No more unused questions in topic: {topic}")
            else:
                print("❌ Invalid topic number!")
        else:
            print("❌ Invalid choice!")

def show_statistics(topic_index, used_questions):
    """Show statistics about question usage."""
    print("\n" + "="*70)
    print("PRACTICE STATISTICS")
    print("="*70)

    total_questions = sum(len(questions) for questions in topic_index.values())
    used_count = len(used_questions)

    print(f"Questions practiced: {used_count}/{total_questions}")
    print(f"Questions remaining: {total_questions - used_count}")
    print(f"Progress: {100*used_count/total_questions:.1f}%")

    print("\nBy topic:")
    for topic in sorted(topic_index.keys()):
        total = len(topic_index[topic])
        used = sum(1 for q in topic_index[topic]
                   if (q['exam'], q['question_id']) in used_questions)
        print(f"  {topic:40s} {used:2d}/{total:2d}")
    print("="*70)

def list_all_questions():
    """List all questions organized by topic."""
    topic_index = build_topic_index()

    print("\n" + "="*70)
    print("ALL QUESTIONS BY TOPIC")
    print("="*70)

    for topic in sorted(topic_index.keys()):
        print(f"\n📌 {topic}")
        print("-" * 70)
        for q in topic_index[topic]:
            print(f"  • {q['exam']} - {q['question_id']}")
            # Print first 60 chars of question
            text_preview = q['text'][:60] + "..." if len(q['text']) > 60 else q['text']
            print(f"    {text_preview}")
        print()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_all_questions()
    else:
        raffle_mode()
