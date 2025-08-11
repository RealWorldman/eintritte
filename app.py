import streamlit as st
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json

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
PASSWORD = st.secrets["APP_PASSWORD"]

# Google Sheets configuration
@st.cache_resource
def init_google_sheets():
    """Initialize Google Sheets connection"""
    try:
        # Get Google Sheets credentials from environment
        creds_dict = st.secrets["GOOGLE_SHEETS_CREDENTIALS"]
        sheet_url = st.secrets["GOOGLE_SHEETS_URL"]
        
        if not creds_dict or not sheet_url:
            return None, None

        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Initialize client and open sheet
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url).sheet1
        
        # Set up headers if sheet is empty
        if not sheet.get_all_values():
            headers = ['Date', 'Time', 'Event', 'Kleinkind', 'Kind', 'Teen', 'Erwachsen', 'Total Amount', 'Payment Method']
            sheet.append_row(headers)
        
        return client, sheet
    except Exception as e:
        st.error(f"Google Sheets connection failed: {str(e)}")
        return None, None

def save_to_google_sheets(sheet, event, cart, total, payment_method):
    """Save sale data to Google Sheets"""
    if not sheet:
        return False
        
    try:
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        
        # Prepare row data
        row_data = [
            date_str,
            time_str,
            EVENTS[event],
            cart.get('kleinkind', 0),
            cart.get('kind', 0),
            cart.get('teen', 0),
            cart.get('erwachsen', 0),
            f"€{total:.2f}",
            payment_method
        ]
        
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"Failed to save to Google Sheets: {str(e)}")
        return False

# Event and ticket configuration
EVENTS = {
    "Freitag": "Freitag",
    "Samstag": "Samstag"
}

TICKET_TYPES = {
    "kleinkind": {"name": "Kleinkinder (unter 6)", "price": 0.00},
    "kind": {"name": "Kinder (6-15)", "price": 6.00},
    "teen": {"name": "Jugendliche (16-17)", "price": 12.00},
    "erwachsen": {"name": "Erwachsene (18+)", "price": 12.00}
}

PAYMENT_METHODS = [
    "💳 Karte",
    "💰 Bar",
    "📱 Twint"
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
    
    # 2x2 grid for event buttons
    event_items = list(EVENTS.items())
    
    # First row
    # col1, col2 = st.columns(2)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if len(event_items) >= 1:
            event_key, event_name = event_items[0]
            if st.button(event_name.replace(' Event', '').replace(' Day', ''), 
                        key=f"event_{event_key}", 
                        use_container_width=True):
                if event_key != st.session_state.selected_event:
                    st.session_state.selected_event = event_key
                    reset_cart()
                    st.rerun()
    
    with col2:
        if len(event_items) >= 2:
            event_key, event_name = event_items[1]
            if st.button(event_name.replace(' Event', '').replace(' Day', ''), 
                        key=f"event_{event_key}", 
                        use_container_width=True):
                if event_key != st.session_state.selected_event:
                    st.session_state.selected_event = event_key
                    reset_cart()
                    st.rerun()
    
    # Second row
    # col3, col4 = st.columns(2)
    with col3:
        if len(event_items) >= 3:
            event_key, event_name = event_items[2]
            if st.button(event_name.replace(' Event', '').replace(' Day', ''), 
                        key=f"event_{event_key}", 
                        use_container_width=True):
                if event_key != st.session_state.selected_event:
                    st.session_state.selected_event = event_key
                    reset_cart()
                    st.rerun()
    
    with col4:
        if len(event_items) >= 4:
            event_key, event_name = event_items[3]
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
    
    # 2x2 grid for ticket selection
    ticket_items = list(TICKET_TYPES.items())
    
    # First row
    col1, col2 = st.columns(2)
    with col1:
        if len(ticket_items) >= 1:
            ticket_key, ticket_info = ticket_items[0]
            st.markdown(f"**{ticket_info['name'].split('(')[0].strip()}**")
            st.markdown(f"€{ticket_info['price']:.0f}")
            
            current_qty = st.session_state.cart.get(ticket_key, 0)
            
            col_minus, col_qty, col_plus = st.columns([1, 2, 1])
            with col_minus:
                if st.button("−1", key=f"minus_{ticket_key}", use_container_width=True):
                    if current_qty > 0:
                        st.session_state.cart[ticket_key] = current_qty - 1
                        st.rerun()
            with col_qty:
                st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; padding: 8px;'>{current_qty}</div>", unsafe_allow_html=True)
            with col_plus:
                if st.button("+1", key=f"plus_{ticket_key}", use_container_width=True):
                    st.session_state.cart[ticket_key] = current_qty + 1
                    st.rerun()
    
    with col2:
        if len(ticket_items) >= 2:
            ticket_key, ticket_info = ticket_items[1]
            st.markdown(f"**{ticket_info['name'].split('(')[0].strip()}**")
            st.markdown(f"€{ticket_info['price']:.0f}")
            
            current_qty = st.session_state.cart.get(ticket_key, 0)
            
            col_minus, col_qty, col_plus = st.columns([1, 2, 1])
            with col_minus:
                if st.button("−1", key=f"minus_{ticket_key}", use_container_width=True):
                    if current_qty > 0:
                        st.session_state.cart[ticket_key] = current_qty - 1
                        st.rerun()
            with col_qty:
                st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; padding: 8px;'>{current_qty}</div>", unsafe_allow_html=True)
            with col_plus:
                if st.button("+1", key=f"plus_{ticket_key}", use_container_width=True):
                    st.session_state.cart[ticket_key] = current_qty + 1
                    st.rerun()
    
    # Second row
    col3, col4 = st.columns(2)
    with col3:
        if len(ticket_items) >= 3:
            ticket_key, ticket_info = ticket_items[2]
            st.markdown(f"**{ticket_info['name'].split('(')[0].strip()}**")
            st.markdown(f"€{ticket_info['price']:.0f}")
            
            current_qty = st.session_state.cart.get(ticket_key, 0)
            
            col_minus, col_qty, col_plus = st.columns([1, 2, 1])
            with col_minus:
                if st.button("−1", key=f"minus_{ticket_key}", use_container_width=True):
                    if current_qty > 0:
                        st.session_state.cart[ticket_key] = current_qty - 1
                        st.rerun()
            with col_qty:
                st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; padding: 8px;'>{current_qty}</div>", unsafe_allow_html=True)
            with col_plus:
                if st.button("+1", key=f"plus_{ticket_key}", use_container_width=True):
                    st.session_state.cart[ticket_key] = current_qty + 1
                    st.rerun()
    
    with col4:
        if len(ticket_items) >= 4:
            ticket_key, ticket_info = ticket_items[3]
            st.markdown(f"**{ticket_info['name'].split('(')[0].strip()}**")
            st.markdown(f"€{ticket_info['price']:.0f}")
            
            current_qty = st.session_state.cart.get(ticket_key, 0)
            
            col_minus, col_qty, col_plus = st.columns([1, 2, 1])
            with col_minus:
                if st.button("−1", key=f"minus_{ticket_key}", use_container_width=True):
                    if current_qty > 0:
                        st.session_state.cart[ticket_key] = current_qty - 1
                        st.rerun()
            with col_qty:
                st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; padding: 8px;'>{current_qty}</div>", unsafe_allow_html=True)
            with col_plus:
                if st.button("+1", key=f"plus_{ticket_key}", use_container_width=True):
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
        
        # Initialize Google Sheets
        try:
            client, sheet = init_google_sheets()
        except Exception as e:
            st.error(f"Failed to initialize Google Sheets: {str(e)}")
            client, sheet = None, None
        
        # Save to Google Sheets
        if sheet:
            success = save_to_google_sheets(sheet, st.session_state.selected_event, st.session_state.cart, total, st.session_state.payment_method)
            if success:
                st.balloons()
                st.success(f"Sale completed! €{total:.0f} - Saved to Google Sheets")
            else:
                st.warning(f"Sale completed! €{total:.0f} - Google Sheets save failed")
        else:
            st.info(f"Sale completed! €{total:.0f} - Google Sheets not configured")
        
        # Auto-reset for next customer but keep event selected
        import time
        time.sleep(1)
        reset_cart()
        # Keep the selected event for next customer
        st.rerun()
    
    # Small action buttons below
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Order", use_container_width=True):
            reset_cart()
            # Keep the event selected for next customer
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
