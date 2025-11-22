import random
import statistics
from typing import List, Optional

# --- Configuration for "Human Preferences" (Weighted Decision Matrix) ---
# These constants represent the monetary value of user comfort/inconvenience.
VALUE_OF_DIRECT_FLIGHT = 60     # Willing to pay $60 to avoid a layover
VALUE_OF_GOOD_TIME = 40         # Willing to pay $40 to avoid 4 AM flights
VALUE_OF_PREMIUM_AIRLINE = 50   # Willing to pay $50 for legroom/snacks
DAILY_PATIENCE_COST = 5         # The cost of waiting 1 extra day (Time Value of Money)

# Days of the week mapping for readable output
DAYS_OF_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

class FlightOption:
    """
    Represents a single flight itinerary with dynamic pricing and attribute generation.
    """
    def __init__(self, day_index: int, base_market_price: int, start_day_offset: int):
        """
        Initialize a flight option with randomized realistic attributes.

        Args:
            day_index (int): The sequential day number in the simulation (0 to N).
            base_market_price (int): The current moving average price of the market.
            start_day_offset (int): Offset to map day_index 0 to a specific day of the week.
        """
        self.day_index = day_index
        
        # 1. Determine Day of Week (0=Mon, 6=Sun)
        # Uses modulo arithmetic to cycle through the week based on the simulation start day.
        current_day_num = (day_index + start_day_offset) % 7
        self.day_name = DAYS_OF_WEEK[current_day_num]
        
        # 2. Airline & Quality Generation
        # Simulates market segmentation: Premium (LuxAir) vs Budget (CheapJet).
        if random.random() < 0.5:
            self.airline = "LuxAir"
            self.quality_bonus = True
            price_modifier = 50
        else:
            self.airline = "CheapJet"
            self.quality_bonus = False
            price_modifier = -30

        # 3. Flight Type (Direct vs Layover)
        # Direct flights are rarer (40% chance) and command a premium.
        if random.random() < 0.40:
            self.is_direct = False # Layover
            price_modifier -= 60   # Layovers are discounted
        else:
            self.is_direct = True
            price_modifier += 20   # Direct flights cost more

        # 4. Calculate Initial Price
        self.price = base_market_price + price_modifier
        
        # 5. REALISM: The "Weekend Tax"
        # Yield management logic: Fri/Sun are high demand, Tue/Wed are low demand.
        if self.day_name in ["Fri", "Sun"]:
            self.price += 80
        elif self.day_name in ["Tue", "Wed"]:
            self.price -= 40 # Mid-week dip

        # 6. REALISM: "Last Minute" Panic Spike
        # Simulates the exponential price increase for booking 0-3 days out.
        if day_index < 3:
            self.price += 150
            
        # 7. Time of Day Logic
        # Adjusts price based on "Prime Time" (mid-day) vs "Red Eye" (early/late).
        hour = random.randint(5, 23)
        self.time_str = f"{hour:02d}:00"
        
        if 10 <= hour <= 16:
            self.time_quality = "Prime"
            self.price += 30
        elif hour < 8 or hour > 20:
            self.time_quality = "Awkward"
            self.price -= 30 # Discount for awkward times
        else:
            self.time_quality = "Standard"

        # Ensure price never drops below a realistic floor
        self.price = max(100, self.price)

    def calculate_score(self) -> int:
        """
        Calculates a 'Total Pain Score' using a Weighted Sum Model.
        
        Formula:
        Score = Price + (Day * Patience_Cost) + Inconvenience_Costs - Comfort_Bonuses
        
        Returns:
            int: The calculated score (Lower is better).
        """
        score = self.price
        
        # Penalties: Add to score (Pain we want to avoid)
        # This adds a "cost of waiting". A cheap flight 30 days away might not be 
        # worth it if patience costs $5/day.
        score += (self.day_index * DAILY_PATIENCE_COST)
        
        # If flight is NOT direct, we add a virtual cost representing the hassle of a layover.
        if not self.is_direct:
            score += VALUE_OF_DIRECT_FLIGHT
            
        # If the time is awkward, we add a virtual cost representing lost sleep/convenience.
        if self.time_quality == "Awkward":
            score += VALUE_OF_GOOD_TIME
            
        # Bonuses: Subtract from score (Comfort reduces the "pain" of the price)
        # If it's a premium airline, we subtract value because the experience is better.
        if self.quality_bonus:
            score -= VALUE_OF_PREMIUM_AIRLINE
            
        return score

def generate_flight_data(days: int = 30) -> List[FlightOption]:
    """
    Generates a list of FlightOption objects for a specified duration.
    Uses a random walk algorithm for the base market price to simulate volatility.
    """
    flights = []
    market_price = random.randint(700, 1100)
    # Random start day (e.g., 0 could be Wednesday instead of Monday)
    start_day_offset = random.randint(0, 6) 
    
    for day in range(days):
        flights.append(FlightOption(day, market_price, start_day_offset))
        
        # Volatility: The market price drifts slightly every day
        market_price += random.randint(-60, 60)
        market_price = max(200, market_price)
        
    return flights

def find_best_flight(flights: List[FlightOption]) -> Optional[FlightOption]:
    """
    Iterates through all flights to find the one with the lowest calculated score.
    
    Args:
        flights (List[FlightOption]): The list of generated flights.
        
    Returns:
        FlightOption: The optimal flight object based on the scoring logic.
    """
    best_flight = None
    lowest_score = float('inf')
    
    for flight in flights:
        score = flight.calculate_score()
        if score < lowest_score:
            lowest_score = score
            best_flight = flight
    return best_flight

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Generate 30 days of flight data
    flight_schedule = generate_flight_data(30)
    
    # 2. Run the optimization algorithm
    best_choice = find_best_flight(flight_schedule)
    
    # 3. Display Results Table
    print(f"\n{'DAY':<4} | {'DOW':<4} | {'AIRLINE':<9} | {'PRICE':<7} | {'SCORE':<6} | {'NOTES'}")
    print("-" * 80)
    
    for f in flight_schedule:
        score = f.calculate_score()
        
        # Visual Helpers for the table
        note = ""
        if f == best_choice:
            note = "✅ WINNER"
        elif f.day_index < 3:
            note = "❌ Last Minute Panic"
        elif f.day_name in ["Fri", "Sun"] and score > f.price:
            note = "⚠️ Weekend Premium"
        elif f.airline == "LuxAir" and score < f.price:
             note = "💎 Luxury Value"
            
        print(f"{f.day_index:<4} | {f.day_name:<4} | {f.airline:<9} | ${f.price:<6} | {score:<6} | {note}")

    # 4. Display Recommendation Summary
    print("-" * 80)
    print(f"🤖 RECOMMENDATION: Day {best_choice.day_index} ({best_choice.day_name}) on {best_choice.airline}")
    print(f"   • Actual Price: ${best_choice.price}")
    print(f"   • Details: {best_choice.time_str}, { 'Direct' if best_choice.is_direct else '1 Stop' }")
    
    if best_choice.airline == "LuxAir":
        print("   • Logic: The premium airline was chosen because the comfort justified the cost.")
    if best_choice.day_name in ["Tue", "Wed"]:
        print("   • Logic: A mid-week flight was selected to avoid weekend surcharges.")
