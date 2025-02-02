import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import calendar


# =========================== #
#         GAME STATE          #
# =========================== #

# Initialize game state
state = {
    "countryName": "",
    "year": 2025,
    "month": 1,
    "popularity": 50,
    "gdp": 15000000,
    "growth": 0.02,
    "medianIncome": 1,
    "meanIncome": 1,
    "lowIncome": 0.5,
    "mediumIncome": 1,
    "highIncome": 1.5,
    "disposableIncome": 1,
    "gdpPerCapita": 1000,
    "interestRate": 0.01,
    "inflation": 0.01,
    "population": 15000,
    "debt": 0,
    "deficit": 0,
    "stockIndex": 100,
    "history": [],
}


# =========================== #
#       GUI CONFIGURATION     #
# =========================== #

# Initialize the main window
root = tk.Tk()
root.title("Economy Simulator")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Main container
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True)

# =========================== #
#    WELCOME SCREEN (Setup)   #
# =========================== #

def start_game():
    country_name = country_entry.get().strip()
    if country_name:
        state["countryName"] = country_name
        welcome_frame.pack_forget()
        show_main_menu()
    else:
        messagebox.showwarning("Input Error", "Please enter a country name.")

welcome_frame = tk.Frame(main_frame, bg="#d9ead3")
welcome_frame.pack(fill="both", expand=True)

welcome_label = tk.Label(welcome_frame, text="Welcome to myEconomyGUI!", font=("Arial", 36), bg="#d9ead3")
welcome_label.pack(pady=50)

country_entry = tk.Entry(welcome_frame, font=("Arial", 24))
country_entry.pack(pady=20)

start_button = tk.Button(welcome_frame, text="Start Game", font=("Arial", 24), command=start_game)
start_button.pack(pady=20)



# =========================== #
#      MANAGE TAXES SCREEN    #
# =========================== #

def manage_taxes():
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    tax_frame = tk.Frame(main_frame, bg="#f9f9f9")
    tax_frame.pack(fill="both", expand=True)

    tk.Label(tax_frame, text="Manage Taxes", font=("Arial", 30), bg="#6fa8dc", fg="white", pady=10).pack(fill="x")

    # Dictionary to store tax rates for each income group
    tax_rates = {
        "Low Income Tax": state.get("lowIncomeTax", 0.1),
        "Medium Income Tax": state.get("mediumIncomeTax", 0.15),
        "High Income Tax": state.get("highIncomeTax", 0.25),
    }

    sliders = {}

    def save_taxes():
        # Update state with new tax values from sliders
        state['lowIncomeTax'] = sliders["Low Income Tax"].get() / 100
        state['mediumIncomeTax'] = sliders["Medium Income Tax"].get() / 100
        state['highIncomeTax'] = sliders["High Income Tax"].get() / 100
        messagebox.showinfo("Taxes Updated", "Tax rates have been updated successfully!")
        tax_frame.pack_forget()
        show_main_menu()

    # Create sliders for each tax category
    for tax_label, initial_value in tax_rates.items():
        frame = tk.Frame(tax_frame, bg="#f9f9f9")
        frame.pack(pady=10)
        
        tk.Label(frame, text=f"{tax_label} (%)", font=("Arial", 18), bg="#f9f9f9").pack(anchor="w", padx=20)
        slider = tk.Scale(frame, from_=0, to=50, orient="horizontal", length=400, resolution=1)
        slider.set(initial_value * 100)
        slider.pack()
        sliders[tax_label] = slider

    # Button to save changes and go back
    save_button = tk.Button(tax_frame, text="Save Changes", font=("Arial", 20), command=save_taxes)
    save_button.pack(pady=20)

    back_button = tk.Button(tax_frame, text="Back to Menu", font=("Arial", 16), command=lambda: [tax_frame.pack_forget(), show_main_menu()])
    back_button.pack()


# =========================== #
#     MANAGE SPENDING SCREEN  #
# =========================== #

def manage_spending():
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    spending_frame = tk.Frame(main_frame, bg="#f9f9f9")
    spending_frame.pack(fill="both", expand=True)

    tk.Label(spending_frame, text="Manage Government Spending", font=("Arial", 30), bg="#6fa8dc", fg="white", pady=10).pack(fill="x")

    # Spending categories with initial values
    spending_categories = {
        "Health Spending": state.get("healthSpending", 0.05),
        "Education Spending": state.get("educationSpending", 0.04),
        "Defence Spending": state.get("defenceSpending", 0.03),
        "Police Spending": state.get("policeSpending", 0.02),
        "Pension Spending": state.get("pensionSpending", 0.05),
        "Subsidies": state.get("subsidies", 0.01),
    }

    sliders = {}

    def save_spending():
        # Update state with new spending values from sliders
        state['healthSpending'] = sliders["Health Spending"].get() / 100
        state['educationSpending'] = sliders["Education Spending"].get() / 100
        state['defenceSpending'] = sliders["Defence Spending"].get() / 100
        state['policeSpending'] = sliders["Police Spending"].get() / 100
        state['pensionSpending'] = sliders["Pension Spending"].get() / 100
        state['subsidies'] = sliders["Subsidies"].get() / 100

        messagebox.showinfo("Spending Updated", "Spending allocations have been updated successfully!")
        spending_frame.pack_forget()
        show_main_menu()

    # Create sliders for each spending category
    for spending_label, initial_value in spending_categories.items():
        frame = tk.Frame(spending_frame, bg="#f9f9f9")
        frame.pack(pady=10)

        tk.Label(frame, text=f"{spending_label} (% of GDP)", font=("Arial", 18), bg="#f9f9f9").pack(anchor="w", padx=20)
        slider = tk.Scale(frame, from_=0, to=50, orient="horizontal", length=400, resolution=1)
        slider.set(initial_value * 100)
        slider.pack()
        sliders[spending_label] = slider

    # Buttons to save changes and go back
    save_button = tk.Button(spending_frame, text="Save Changes", font=("Arial", 20), command=save_spending)
    save_button.pack(pady=20)

    back_button = tk.Button(spending_frame, text="Back to Menu", font=("Arial", 16), command=lambda: [spending_frame.pack_forget(), show_main_menu()])
    back_button.pack()


# =========================== #
#        FINANCE SCREEN       #
# =========================== #

def manage_finance():
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    finance_frame = tk.Frame(main_frame, bg="#f9f9f9")
    finance_frame.pack(fill="both", expand=True)

    tk.Label(finance_frame, text="Manage Finance", font=("Arial", 30), bg="#6fa8dc", fg="white", pady=10).pack(fill="x")

    # Display current debt and deficit
    debt_label = tk.Label(finance_frame, text=f"Current Debt: ${state['debt']:,}", font=("Arial", 20), bg="#f9f9f9")
    debt_label.pack(pady=10)

    deficit_label = tk.Label(finance_frame, text=f"Current Deficit: ${state['deficit']:,}", font=("Arial", 20), bg="#f9f9f9")
    deficit_label.pack(pady=10)

    # Interest Rate Slider
    tk.Label(finance_frame, text="Adjust Interest Rate (%)", font=("Arial", 18), bg="#f9f9f9").pack(pady=10)
    interest_rate_slider = tk.Scale(finance_frame, from_=0, to=20, orient="horizontal", length=400, resolution=0.1)
    interest_rate_slider.set(state.get("interestRate", 0.01) * 100)  # Convert to percentage
    interest_rate_slider.pack()

    # Debt Payment Entry
    tk.Label(finance_frame, text="Make a Debt Payment ($)", font=("Arial", 18), bg="#f9f9f9").pack(pady=10)
    debt_payment_entry = tk.Entry(finance_frame, font=("Arial", 16))
    debt_payment_entry.pack()

    # Save Finance Changes
    def save_finance():
        # Update interest rate
        state["interestRate"] = interest_rate_slider.get() / 100  # Convert back to decimal

        # Handle debt payment
        try:
            payment = float(debt_payment_entry.get())
            if payment > 0:
                if payment <= state["gdp"]:  # Ensure payment isn't more than GDP
                    state["debt"] = max(0, state["debt"] - payment)
                    messagebox.showinfo("Payment Successful", f"Paid ${payment:,.2f} towards the debt.")
                else:
                    messagebox.showwarning("Invalid Payment", "Payment exceeds GDP.")
        except ValueError:
            pass  # Ignore invalid input

        finance_frame.pack_forget()
        show_main_menu()

    save_button = tk.Button(finance_frame, text="Save Changes", font=("Arial", 20), command=save_finance)
    save_button.pack(pady=20)

    back_button = tk.Button(finance_frame, text="Back to Menu", font=("Arial", 16), command=lambda: [finance_frame.pack_forget(), show_main_menu()])
    back_button.pack()


# =========================== #
#      NEXT MONTH LOGIC       #
# =========================== #

def next_month():
    # Advance the date
    state["month"] += 1
    if state["month"] > 12:
        state["month"] = 1
        state["year"] += 1

    # === ECONOMIC SIMULATION === #
    # 1. GDP Growth Calculation
    investment = state["educationSpending"] * 0.1 - state["interestRate"] * 0.05
    tax_effect = -(state["lowIncomeTax"] + state["mediumIncomeTax"] + state["highIncomeTax"]) * 0.02
    spending_effect = (state["healthSpending"] + state["educationSpending"] + state["subsidies"]) * 0.03

    gdp_growth = state["growth"] + investment + tax_effect + spending_effect
    gdp_growth = max(-0.05, min(0.05, gdp_growth))  # Limit growth to ±5%

    state["gdp"] *= (1 + gdp_growth)

    # 2. Population Growth
    population_growth = 0.01 + state["healthSpending"] * 0.02
    state["population"] = int(state["population"] * (1 + population_growth / 12))

    # 3. Debt and Deficit
    revenue = (
        state["lowIncomeTax"] * 0.1 * state["gdp"] +
        state["mediumIncomeTax"] * 0.3 * state["gdp"] +
        state["highIncomeTax"] * 0.6 * state["gdp"]
    )
    spending = (
        state["healthSpending"] + state["educationSpending"] +
        state["defenceSpending"] + state["policeSpending"] +
        state["pensionSpending"] + state["subsidies"]
    ) * state["gdp"]

    state["deficit"] = spending - revenue
    state["debt"] += state["deficit"]

    # 4. Inflation Adjustment
    inflation_effect = (state["interestRate"] - 0.02) * -0.5
    state["inflation"] = max(0, state["inflation"] + inflation_effect)

    # 5. Popularity Change
    if state["deficit"] > 0:
        state["popularity"] -= 1
    else:
        state["popularity"] += 1
    state["popularity"] = max(0, min(100, state["popularity"]))

    # 6. Save History for Graphs
    state["history"].append({
        "date": f"{calendar.month_name[state['month']]}, {state['year']}",
        "gdp": state["gdp"],
        "population": state["population"],
        "deficit": state["deficit"],
        "debt": state["debt"],
        "inflation": state["inflation"],
        "popularity": state["popularity"]
    })


    # Refresh the main menu to show updated stats
    for widget in main_frame.winfo_children():
        widget.destroy()
    show_main_menu()
    
    trigger_random_event()
    autosave()

# =========================== #
#         VIEW STATS          #
# =========================== #

from matplotlib.ticker import FuncFormatter

# Helper function to format large numbers
def human_readable_format(value, _):
    if value >= 1e9:
        return f"{value / 1e9:.1f}B"  # Billions
    elif value >= 1e6:
        return f"{value / 1e6:.1f}M"  # Millions
    elif value >= 1e3:
        return f"{value / 1e3:.1f}K"  # Thousands
    else:
        return str(int(value))        # Regular numbers

def view_stats():
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    stats_frame = tk.Frame(main_frame, bg="#f9f9f9")
    stats_frame.pack(fill="both", expand=True)

    tk.Label(stats_frame, text="Economic Statistics", font=("Arial", 30), bg="#6fa8dc", fg="white", pady=10).pack(fill="x")

    # Dropdown to select which stat to view
    stats_options = ["GDP", "Population", "Deficit", "Debt", "Inflation", "Popularity"]
    selected_stat = tk.StringVar()
    selected_stat.set(stats_options[0])  # Default option

    dropdown = ttk.Combobox(stats_frame, textvariable=selected_stat, values=stats_options, font=("Arial", 16))
    dropdown.pack(pady=20)

    # Button to display the selected graph
    def plot_stat():
        stat = selected_stat.get().lower()
        dates = [entry["date"] for entry in state["history"]]
        values = [entry[stat] for entry in state["history"]]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, marker='o', markersize=4, color='blue')

        plt.title(f"{stat.capitalize()} Over Time", fontsize=16)
        plt.xlabel("Date", fontsize=14)
        plt.ylabel(stat.capitalize(), fontsize=14)

        # Apply human-readable formatting to y-axis
        ax = plt.gca()
        ax.yaxis.set_major_formatter(FuncFormatter(human_readable_format))
        plt.xticks(rotation=45)
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    plot_button = tk.Button(stats_frame, text="Show Graph", font=("Arial", 18), command=plot_stat)
    plot_button.pack(pady=10)

    # Back to Menu Button
    back_button = tk.Button(stats_frame, text="Back to Menu", font=("Arial", 16), command=lambda: [stats_frame.pack_forget(), show_main_menu()])
    back_button.pack(pady=10)

# =========================== #
#       SAVE GAME LOGIC       #
# =========================== #

def save_game():
    # Create a filename based on the current date and time
    filename = f"save_{state['countryName']}_{state['year']}_{state['month']}.json"

    # Save the state dictionary to a JSON file
    with open(filename, "w") as file:
        json.dump(state, file)

    messagebox.showinfo("Game Saved", f"Game saved as {filename}!")

# =========================== #
#       LOAD GAME LOGIC       #
# =========================== #

def load_game():
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    load_frame = tk.Frame(main_frame, bg="#f9f9f9")
    load_frame.pack(fill="both", expand=True)

    tk.Label(load_frame, text="Load Saved Game", font=("Arial", 30), bg="#6fa8dc", fg="white", pady=10).pack(fill="x")

    # List all saved files in the current directory
    save_files = [f for f in os.listdir() if f.startswith("save_") and f.endswith(".json")]
    save_files.sort(key=os.path.getmtime, reverse=True)  # Sort by latest saves

    if not save_files:
        tk.Label(load_frame, text="No save files found.", font=("Arial", 18)).pack(pady=20)
    else:
        # Display up to 10 recent saves
        for save_file in save_files[:10]:
            def load_selected(file=save_file):
                with open(file, "r") as f:
                    loaded_data = json.load(f)
                    state.update(loaded_data)
                messagebox.showinfo("Game Loaded", f"Game loaded from {file}")
                load_frame.pack_forget()
                show_main_menu()

            button = tk.Button(load_frame, text=save_file, font=("Arial", 16), command=load_selected)
            button.pack(pady=5)

    # Back to Menu Button
    back_button = tk.Button(load_frame, text="Back to Menu", font=("Arial", 16), command=lambda: [load_frame.pack_forget(), show_main_menu()])
    back_button.pack(pady=20)

# =========================== #
#     AUTOSAVE FUNCTIONALITY  #
# =========================== #

def autosave():
    filename = f"autosave_{state['countryName']}.json"
    with open(filename, "w") as file:
        json.dump(state, file)


# =========================== #
#        RANDOM EVENTS        #
# =========================== #

# Define random events
events = [
    {
        "name": "Recession",
        "description": "A global recession has hit, reducing economic growth and tax revenue.",
        "effects": {
            "gdp_multiplier": 0.95,
            "popularity_change": -5,
            "inflation_change": -0.01
        }
    },
    {
        "name": "Economic Boom",
        "description": "The economy is booming with record growth and investor confidence!",
        "effects": {
            "gdp_multiplier": 1.05,
            "popularity_change": 3,
            "inflation_change": 0.02
        }
    },
    {
        "name": "Pandemic",
        "description": "A pandemic has spread, causing reduced productivity and population growth.",
        "effects": {
            "gdp_multiplier": 0.9,
            "popularity_change": -10,
            "population_growth_multiplier": 0.95
        }
    },
    {
        "name": "Stock Market Crash",
        "description": "A sudden stock market crash has shaken investor confidence.",
        "effects": {
            "gdp_multiplier": 0.97,
            "popularity_change": -3,
            "inflation_change": -0.02
        }
    },
    {
        "name": "Natural Disaster",
        "description": "A major natural disaster has caused widespread damage, reducing productivity.",
        "effects": {
            "gdp_multiplier": 0.92,
            "popularity_change": -7,
            "deficit_increase": 1000000  # Example cost of disaster relief
        }
    }
]

# Trigger a random event with a 10% chance each month
def trigger_random_event():
    if random.random() < 0.1:  # 10% chance
        event = random.choice(events)
        effects = event["effects"]

        # Apply event effects
        state["gdp"] *= effects.get("gdp_multiplier", 1)
        state["popularity"] += effects.get("popularity_change", 0)
        state["inflation"] += effects.get("inflation_change", 0)
        state["deficit"] += effects.get("deficit_increase", 0)

        # Apply population growth effect if present
        if "population_growth_multiplier" in effects:
            state["population"] = int(state["population"] * effects["population_growth_multiplier"])

        # Ensure limits are respected
        state["popularity"] = max(0, min(100, state["popularity"]))
        state["inflation"] = max(0, state["inflation"])

        # Show the event to the player
        messagebox.showinfo(f"Event: {event['name']}", event["description"])


# =========================== #
#   LOAD EVENTS FROM JSON     #
# =========================== #

def load_events():
    try:
        with open("events.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "events.json file not found.")
        return []

events = load_events()

# =========================== #
#    TRIGGER CUSTOM EVENTS    #
# =========================== #

def trigger_random_event():
    if random.random() < 0.2:  # 20% chance
        event = random.choice(events)
        effects = event["effects"]

        # Apply event effects
        state["gdp"] *= effects.get("gdp_multiplier", 1)
        state["popularity"] += effects.get("popularity_change", 0)
        state["inflation"] += effects.get("inflation_change", 0)
        state["deficit"] += effects.get("deficit_increase", 0)

        if "population_growth_multiplier" in effects:
            state["population"] = int(state["population"] * effects["population_growth_multiplier"])

        # Ensure limits are respected
        state["popularity"] = max(0, min(100, state["popularity"]))
        state["inflation"] = max(0, state["inflation"])

        messagebox.showinfo(f"Event: {event['name']}", event["description"])

# ===================== #
#    QUALITY OF LIFE    #
# ===================== #

# Add tooltips to buttons for extra context
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()  # Hide initially
    tooltip.overrideredirect(True)
    tooltip_label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1, font=("Arial", 10))
    tooltip_label.pack()

    def show_tooltip(event):
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        tooltip.deiconify()

    def hide_tooltip(event):
        tooltip.withdraw()

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

# Example for adding tooltips:
# In show_main_menu():
# create_tooltip(tax_button, "Adjust income tax rates for different classes.")

# Confirmation dialog when quitting the game
def confirm_quit():
    if messagebox.askokcancel("Quit Game", "Are you sure you want to quit?"):
        root.destroy()


# Make the app responsive to window resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_frame.grid(sticky="nsew")  # Stretch to fill window

# Add gridlines and smooth curves in stats graphs
def plot_stat():
    stat = selected_stat.get().lower()
    dates = [entry["date"] for entry in state["history"]]
    values = [entry[stat] for entry in state["history"]]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o', markersize=4, color='blue', linestyle='-', linewidth=2)

    plt.grid(True, linestyle='--', alpha=0.6)  # Add gridlines
    plt.title(f"{stat.capitalize()} Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel(stat.capitalize(), fontsize=14)

    plt.tight_layout()
    plt.show()
    
# =========================== #
#       MAIN GAME MENU        #
# =========================== #

def show_main_menu():
    # Frame for the main dashboard
    dashboard_frame = tk.Frame(main_frame, bg="#f0f0f0")
    dashboard_frame.pack(fill="both", expand=True)

    # Header with country name and date
    header = tk.Label(
        dashboard_frame,
        text=f"{state['countryName']} - {calendar.month_name[state['month']]}, {state['year']}",
        font=("Arial", 30),
        bg="#6fa8dc",
        fg="white",
        padx=20,
        pady=10
    )
    header.pack(fill="x")

    # Stats Display
    stats_text = tk.StringVar()
    stats_text.set(f"GDP: ${state['gdp']:,} | Population: {state['population']} | Inflation: {state['inflation']*100:.2f}% | Deficit: {state['deficit']}")

    stats_label = tk.Label(dashboard_frame, textvariable=stats_text, font=("Arial", 20), bg="#f0f0f0")
    stats_label.pack(pady=20)

    # Buttons for game actions
    button_frame = tk.Frame(dashboard_frame, bg="#f0f0f0")
    button_frame.pack()

    buttons = [
        ("Manage Taxes", manage_taxes),
        ("Manage Spending", manage_spending),
        ("Adjust Finance", manage_finance),
        ("View Stats", view_stats),
        ("Next Month", next_month),
        ("Save Game", save_game),
        ("Load Game", load_game),
        ("Quit Game", confirm_quit)
    ]
    for (text, command) in buttons:
        btn = tk.Button(button_frame, text=text, font=("Arial", 18), width=20, command=command)
        btn.pack(pady=5)
        
        
# =========================== #
#        MAIN LOOP            #
# =========================== #

root.mainloop()


