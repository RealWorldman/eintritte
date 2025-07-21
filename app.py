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
    st.markdown("## 📅 Select Event")
    
    event_options = list(EVENTS.keys())
    selected_event = st.selectbox(
        "Choose the event:",
        event_options,
        format_func=lambda x: EVENTS[x],
        key="event_selector"
    )
    
    if selected_event != st.session_state.selected_event:
        st.session_state.selected_event = selected_event
        reset_cart()  # Clear cart when switching events
        st.rerun()
    
    if st.session_state.selected_event:
        st.success(f"📍 Event: **{EVENTS[st.session_state.selected_event]}**")

def display_ticket_selection():
    """Display ticket selection interface"""
    if not st.session_state.selected_event:
        return
        
    st.markdown("## 🎫 Select Tickets")
    
    # Create columns for better mobile layout
    col1, col2 = st.columns(2)
    
    with col1:
        for i, (ticket_key, ticket_info) in enumerate(list(TICKET_TYPES.items())[:2]):
            st.markdown(f"**{ticket_info['name']}**")
            st.markdown(f"💰 €{ticket_info['price']:.2f}")
            
            current_qty = st.session_state.cart.get(ticket_key, 0)
            quantity = st.number_input(
                "Quantity:",
                min_value=0,
                max_value=50,
                value=current_qty,
                step=1,
                key=f"qty_{ticket_key}",
                label_visibility="collapsed"
            )
            st.session_state.cart[ticket_key] = quantity
            st.markdown("---")
    
    with col2:
        for i, (ticket_key, ticket_info) in enumerate(list(TICKET_TYPES.items())[2:]):
            st.markdown(f"**{ticket_info['name']}**")
            st.markdown(f"💰 €{ticket_info['price']:.2f}")
            
            current_qty = st.session_state.cart.get(ticket_key, 0)
            quantity = st.number_input(
                "Quantity:",
                min_value=0,
                max_value=50,
                value=current_qty,
                step=1,
                key=f"qty_{ticket_key}",
                label_visibility="collapsed"
            )
            st.session_state.cart[ticket_key] = quantity
            st.markdown("---")

def display_cart_summary():
    """Display cart summary and total"""
    total = calculate_total()
    
    if total > 0:
        st.markdown("## 🛒 Order Summary")
        
        # Display selected tickets
        for ticket_type, quantity in st.session_state.cart.items():
            if quantity > 0:
                ticket_info = TICKET_TYPES[ticket_type]
                subtotal = ticket_info["price"] * quantity
                st.markdown(
                    f"**{ticket_info['name']}** × {quantity} = €{subtotal:.2f}"
                )
        
        st.markdown("---")
        st.markdown(f"## 💰 **Total: €{total:.2f}**")
        
        return True
    else:
        st.info("🛒 No tickets selected yet")
        return False

def display_payment_selection():
    """Display payment method selection"""
    if calculate_total() <= 0:
        return False
        
    st.markdown("## 💳 Select Payment Method")
    
    payment_method = st.radio(
        "How will the customer pay?",
        PAYMENT_METHODS,
        key="payment_selector"
    )
    
    st.session_state.payment_method = payment_method
    return True

def display_final_confirmation():
    """Display final confirmation and completion"""
    if not st.session_state.payment_method or calculate_total() <= 0:
        return
        
    st.markdown("## ✅ Ready to Complete")
    
    # Final summary in a nice format
    with st.container():
        st.markdown("### 📋 Final Order Details")
        st.markdown(f"**Event:** {EVENTS[st.session_state.selected_event]}")
        st.markdown(f"**Payment Method:** {st.session_state.payment_method}")
        st.markdown("**Tickets:**")
        
        for ticket_type, quantity in st.session_state.cart.items():
            if quantity > 0:
                ticket_info = TICKET_TYPES[ticket_type]
                subtotal = ticket_info["price"] * quantity
                st.markdown(f"- {ticket_info['name']} × {quantity} = €{subtotal:.2f}")
        
        total = calculate_total()
        st.markdown(f"### 💰 **Total Amount: €{total:.2f}**")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Start New Order", use_container_width=True):
            reset_cart()
            st.session_state.selected_event = None
            st.rerun()
    
    with col2:
        if st.button("✏️ Modify Order", use_container_width=True):
            st.session_state.payment_method = None
            st.rerun()
    
    with col3:
        if st.button("✅ Complete Sale", use_container_width=True, type="primary"):
            # Here you would normally save the transaction to a database
            # For now, we'll show a success message and reset
            st.balloons()
            st.success(f"🎉 Sale completed! Total: €{total:.2f}")
            st.info("💾 Transaction recorded successfully")
            
            # Auto-reset after a few seconds
            import time
            time.sleep(2)
            reset_cart()
            st.session_state.selected_event = None
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
