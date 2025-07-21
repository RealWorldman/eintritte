import streamlit as st
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Sports Club Ticket Sales",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'selected_event' not in st.session_state:
    st.session_state.selected_event = None
if 'payment_method' not in st.session_state:
    st.session_state.payment_method = None

# Configuration
PASSWORD = os.getenv("APP_PASSWORD", "sportsclub2024")

# Event and ticket configuration
EVENTS = {
    "Friday-Day": "Friday Day Event",
    "Saturday-Event": "Saturday Main Event", 
    "Sunday-Family": "Sunday Family Day",
    "VIP-Experience": "VIP Experience Package"
}

TICKET_TYPES = {
    "kids": {"name": "Kids (Under 12)", "price": 8.00},
    "young_adults": {"name": "Young Adults (12-17)", "price": 12.00},
    "adults": {"name": "Adults (18+)", "price": 18.00},
    "seniors": {"name": "Seniors (65+)", "price": 15.00}
}

PAYMENT_METHODS = [
    "💳 Credit Card",
    "💰 Cash", 
    "📱 Mobile Payment",
    "🏦 Bank Transfer",
    "🎫 Voucher"
]

def authenticate():
    """Handle password authentication"""
    st.title("🏆 Sports Club Event Tickets")
    st.markdown("### Please enter the access password")
    
    password_input = st.text_input("Password", type="password", key="password_input")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔓 Access System", use_container_width=True):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Access granted!")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")

def reset_cart():
    """Reset the shopping cart"""
    st.session_state.cart = {}
    st.session_state.payment_method = None

def calculate_total():
    """Calculate total price of items in cart"""
    total = 0
    for ticket_type, quantity in st.session_state.cart.items():
        if quantity > 0:
            total += TICKET_TYPES[ticket_type]["price"] * quantity
    return total

def display_event_selection():
    """Display event selection interface"""
    st.markdown("**Event:**")
    
    # Compact event buttons
    cols = st.columns(len(EVENTS))
    event_items = list(EVENTS.items())
    
    for i, (event_key, event_name) in enumerate(event_items):
        with cols[i]:
            if st.button(event_name.replace(' Event', '').replace(' Day', ''), 
                        key=f"event_{event_key}", 
                        use_container_width=True):
                if event_key != st.session_state.selected_event:
                    st.session_state.selected_event = event_key
                    reset_cart()
                    st.rerun()
    
    if st.session_state.selected_event:
        st.info(f"Event: {EVENTS[st.session_state.selected_event]}")

def display_ticket_selection():
    """Display ticket selection interface"""
    if not st.session_state.selected_event:
        return
        
    st.markdown("## 🎫 Tickets")
    
    # Compact horizontal layout for all tickets
    cols = st.columns(len(TICKET_TYPES))
    
    for i, (ticket_key, ticket_info) in enumerate(TICKET_TYPES.items()):
        with cols[i]:
            st.markdown(f"**{ticket_info['name'].split('(')[0].strip()}**")
            st.markdown(f"€{ticket_info['price']:.0f}")
            
            current_qty = st.session_state.cart.get(ticket_key, 0)
            
            # Use + and - buttons for faster entry
            col_minus, col_qty, col_plus = st.columns([1, 2, 1])
            
            with col_minus:
                if st.button("−", key=f"minus_{ticket_key}", use_container_width=True):
                    if current_qty > 0:
                        st.session_state.cart[ticket_key] = current_qty - 1
                        st.rerun()
            
            with col_qty:
                st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; padding: 8px;'>{current_qty}</div>", unsafe_allow_html=True)
            
            with col_plus:
                if st.button("+", key=f"plus_{ticket_key}", use_container_width=True):
                    st.session_state.cart[ticket_key] = current_qty + 1
                    st.rerun()

def display_cart_summary():
    """Display cart summary and total"""
    total = calculate_total()
    
    if total > 0:
        # Compact summary in single line format
        summary_parts = []
        for ticket_type, quantity in st.session_state.cart.items():
            if quantity > 0:
                ticket_name = TICKET_TYPES[ticket_type]["name"].split('(')[0].strip()
                summary_parts.append(f"{ticket_name}: {quantity}")
        
        if summary_parts:
            st.markdown(f"**Items:** {' | '.join(summary_parts)}")
            st.markdown(f"# **€{total:.0f}**")
        
        return True
    else:
        return False

def display_payment_selection():
    """Display payment method selection"""
    if calculate_total() <= 0:
        return False
        
    st.markdown("**Payment:**")
    
    # Compact button layout for payment methods
    cols = st.columns(len(PAYMENT_METHODS))
    
    for i, method in enumerate(PAYMENT_METHODS):
        with cols[i]:
            method_name = method.split(' ', 1)[1]  # Remove emoji for button text
            if st.button(method_name, key=f"pay_{i}", use_container_width=True):
                st.session_state.payment_method = method
                st.rerun()
    
    if st.session_state.payment_method:
        st.success(f"Payment: {st.session_state.payment_method}")
        return True
    
    return False

def display_final_confirmation():
    """Display final confirmation and completion"""
    if not st.session_state.payment_method or calculate_total() <= 0:
        return
        
    # Large complete sale button
    if st.button("✅ COMPLETE SALE", use_container_width=True, type="primary"):
        total = calculate_total()
        st.balloons()
        st.success(f"Sale completed! €{total:.0f}")
        
        # Auto-reset for next customer
        import time
        time.sleep(1)
        reset_cart()
        st.session_state.selected_event = None
        st.rerun()
    
    # Small action buttons below
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Order", use_container_width=True):
            reset_cart()
            st.session_state.selected_event = None
            st.rerun()
    
    with col2:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.payment_method = None
            st.rerun()

def main():
    """Main application logic"""
    
    if not st.session_state.authenticated:
        authenticate()
        return
    
    # Header
    st.title("🏆 Sports Club Ticket Sales")
    st.markdown(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown("### System Actions")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.cart = {}
            st.session_state.selected_event = None
            st.session_state.payment_method = None
            st.rerun()
        
        if st.button("🔄 Reset All"):
            reset_cart()
            st.session_state.selected_event = None
            st.rerun()
    
    # Main workflow
    display_event_selection()
    
    if st.session_state.selected_event:
        display_ticket_selection()
        
        if display_cart_summary():
            if display_payment_selection():
                display_final_confirmation()

if __name__ == "__main__":
    main()
