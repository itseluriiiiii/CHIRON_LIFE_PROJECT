from flask import Flask, render_template, request
import google.generativeai as genai
import os

# Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDPwxIV4Cm83RCJP8tObNlooisyesN6B9E"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

app = Flask(__name__)

# Initialize the model
model = genai.GenerativeModel("models/gemini-pro")

# Function to generate recommendations
def generate_recommendation(age, gender, weight, height, region, dietary_preferences, fitness_goals, lifestyle_factors,
                            dietary_restrictions, health_conditions, user_query):
    prompt = f"""
    Suggest a comprehensive plan including diet and workout options based on the following details:
    Age: {age},
    Gender: {gender},
    Weight: {weight},
    Height: {height},
    Region: {region},
    Dietary Preferences: {dietary_preferences},
    Fitness Goals: {fitness_goals},
    Lifestyle Factors: {lifestyle_factors},
    Dietary Restrictions: {dietary_restrictions},
    Health Conditions: {health_conditions},
    User Query: {user_query}.

    Based on this information, create a customized plan including:

    Diet Recommendations: RETURN LIST
    - 5 specific diet types suited to their preferences and goals.

    Workout Options: RETURN LIST
    - 5 workout recommendations that align with their fitness level and goals.

    Meal Suggestions: RETURN LIST
    - 5 breakfast ideas.
    - 5 dinner options.

    Additional Recommendations: RETURN LIST
    - Any useful snacks, supplements, or hydration tips tailored to their profile.
    """

    response = model.generate_content(prompt)
    return response.text if response else "No response from the model."

@app.route('/')
def index():
    return render_template('index.html', recommendations=None)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        region = request.form['region']
        dietary_preferences = request.form['dietary_preferences']
        fitness_goals = request.form['fitness_goals']
        lifestyle_factors = request.form['lifestyle_factors']
        dietary_restrictions = request.form['dietary_restrictions']
        health_conditions = request.form['health_conditions']
        user_query = request.form['user_query']

        recommendations_text = generate_recommendation(
            age, gender, weight, height, region, dietary_preferences, fitness_goals,
            lifestyle_factors, dietary_restrictions, health_conditions, user_query
        ) #accept values from user

     #results 
        recommendations = {
            "diet_types": [],
            "workouts": [],
            "breakfasts": [],
            "dinners": [],
            "additional_tips": []
        }

        # Split and map responses based on keywords
        current_section = None
        for line in recommendations_text.splitlines():
            if "Diet Recommendations:" in line:
                current_section = "diet_types"
            elif "Workout Options:" in line:
                current_section = "workouts"
            elif "Meal Suggestions:" in line:
                current_section = "breakfasts"
            elif "Dinner Options:" in line:
                current_section = "dinners"
            elif "Additional Recommendations:" in line:
                current_section = "additional_tips"
            elif line.strip() and current_section:
                recommendations[current_section].append(line.strip())

        return render_template('index.html', recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)