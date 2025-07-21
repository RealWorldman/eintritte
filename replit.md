# Sports Club Ticket Sales System

## Overview

This is a Streamlit-based web application for managing sports club ticket sales. The system provides a user-friendly interface for customers to browse events, select tickets, and complete purchases. It features a simple authentication mechanism and shopping cart functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid development and built-in UI components
- **Layout**: Wide layout with collapsed sidebar for better user experience
- **State Management**: Streamlit session state for maintaining user data across interactions
- **Responsive Design**: Leverages Streamlit's native responsive capabilities

### Backend Architecture
- **Runtime**: Python-based single-file application
- **Session Management**: In-memory session state (non-persistent)
- **Authentication**: Simple password-based authentication using environment variables
- **Data Storage**: In-memory data structures (dictionaries) for events and ticket types

### Security Model
- **Authentication**: Single shared password stored in environment variable
- **Session State**: Temporary authentication state per user session
- **Environment Configuration**: Password configurable via `APP_PASSWORD` environment variable

## Key Components

### Authentication System
- Simple password gate using `authenticate()` function
- Default password: "sportsclub2024" (configurable via environment)
- Session-based authentication state tracking

### Event Management
- Predefined event catalog with 4 main events:
  - Friday Day Event
  - Saturday Main Event
  - Sunday Family Day
  - VIP Experience Package
- Static event configuration stored in `EVENTS` dictionary

### Ticket System
- Four ticket categories with different pricing:
  - Kids (Under 12): $8.00
  - Young Adults (12-17): $12.00
  - Adults (18+): $18.00
  - Seniors (65+): $15.00
- Configurable ticket types in `TICKET_TYPES` dictionary

### Shopping Cart
- Session-based cart storage
- Support for multiple ticket types per transaction
- Cart state maintained in `st.session_state.cart`

### Payment Processing
- Multiple payment method options:
  - Credit Card
  - Cash
  - Mobile Payment
  - Bank Transfer
  - Voucher
- Payment method selection stored in session state

## Data Flow

1. **Authentication Flow**: User enters password → System validates → Sets authentication state
2. **Event Selection**: User browses events → Selects event → Updates session state
3. **Ticket Selection**: User selects ticket types and quantities → Updates cart
4. **Payment Flow**: User selects payment method → Processes transaction
5. **Session Management**: All data maintained in Streamlit session state throughout user journey

## External Dependencies

### Python Packages
- **Streamlit**: Web application framework and UI components
- **os**: Environment variable access for configuration
- **datetime**: Date/time handling for transactions and events

### Environment Variables
- `APP_PASSWORD`: Configurable authentication password (defaults to "sportsclub2024")

### Runtime Requirements
- Python 3.x environment
- Streamlit server capabilities
- Web browser for user interface

## Deployment Strategy

### Development Environment
- Single Python file deployment (`app.py`)
- Streamlit development server for local testing
- Environment variable configuration for different environments

### Production Considerations
- **Scalability Limitation**: In-memory storage not suitable for multi-user production
- **State Persistence**: Session data lost on server restart
- **Security**: Shared password model not suitable for production use
- **Recommended Upgrades**: Database integration, proper user authentication, persistent storage

### Deployment Options
- **Local Development**: `streamlit run app.py`
- **Cloud Platforms**: Compatible with Streamlit Cloud, Heroku, or containerized deployments
- **Configuration**: Environment variables for password and other settings

## Technical Debt and Future Enhancements

### Current Limitations
- No persistent data storage
- Single shared password authentication
- In-memory cart and session management
- No transaction history or audit trail

### Recommended Improvements
- Database integration for persistent storage
- User registration and individual authentication
- Payment gateway integration
- Admin dashboard for event and ticket management
- Email confirmation and ticket generation
- Inventory management and sold-out handling

## Recent Changes

### July 21, 2025
- **Compact Interface Design**: Redesigned all UI elements for faster entry at event gates
  - Changed ticket selection to + and - buttons for quicker entry
  - Converted event selection to horizontal button layout
  - Simplified order summary to single line with total
  - Made payment methods clickable buttons in horizontal layout
  - Added large "COMPLETE SALE" button for quick checkout
- **Persistent Event Selection**: Event choice now persists between sales to avoid reselection
- **Auto-Reset Optimization**: Cart clears after each sale but keeps event selected for next customer
- **Google Sheets Integration**: All sales data automatically saved to Google Sheets with timestamp, event details, ticket quantities, total amount, and payment method