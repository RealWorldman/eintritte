# Sports Club Ticket Sales System

A compact, mobile-friendly Streamlit web application for managing sports club event ticket sales at entry points. Designed for fast customer processing with automatic Google Sheets integration for sales tracking.

## Features

- **Password Protection**: Secure access to the sales system
- **Event Management**: Quick selection from multiple events (Friday Day, Saturday Event, Sunday Family, VIP Experience)
- **Ticket Types**: Support for Kids, Young Adults, Adults, and Seniors with different pricing
- **Compact Interface**: 2x2 grid layout optimized for mobile/tablet use at entry gates
- **Fast Entry**: + and - buttons for quick ticket quantity selection
- **Payment Methods**: Multiple payment options (Credit Card, Cash, Mobile Payment, Bank Transfer, Voucher)
- **Google Sheets Integration**: Automatic saving of all sales data with timestamps
- **Persistent Event Selection**: Event choice remains selected between customers for faster processing

## Quick Start

1. Clone this repository
2. Install dependencies: `pip install streamlit gspread google-auth`
3. Set up environment variables (see Configuration section)
4. Run: `streamlit run app.py --server.port 5000`

## Configuration

### Environment Variables

- `APP_PASSWORD`: Access password for the system (default: "sportsclub2024")
- `GOOGLE_SHEETS_CREDENTIALS`: JSON credentials from Google Cloud Console
- `GOOGLE_SHEETS_URL`: URL of your Google Sheet for sales data

### Google Sheets Setup

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account and download JSON credentials
4. Create a new Google Sheet
5. Share the sheet with your service account email
6. Add the credentials and sheet URL to your environment variables

## Usage

1. **Login**: Enter the configured password
2. **Select Event**: Choose from the 2x2 grid of available events
3. **Add Tickets**: Use + and - buttons to select ticket quantities
4. **Choose Payment**: Click on the payment method
5. **Complete Sale**: Hit the large "COMPLETE SALE" button

The system automatically:
- Saves sale data to Google Sheets
- Resets the cart for the next customer
- Keeps the event selected for faster processing

## File Structure

```
├── app.py              # Main Streamlit application
├── .streamlit/
│   └── config.toml     # Streamlit configuration
├── pyproject.toml      # Python dependencies
├── replit.md          # Project documentation
└── README.md          # This file
```

## Data Storage

Sales data is automatically saved to Google Sheets with the following columns:
- Date
- Time
- Event
- Kids (quantity)
- Young Adults (quantity)
- Adults (quantity)
- Seniors (quantity)
- Total Amount
- Payment Method

## Deployment

### Local Development
```bash
streamlit run app.py --server.port 5000
```

### Cloud Deployment
Compatible with:
- Streamlit Cloud
- Heroku
- Replit
- Any platform supporting Python and Streamlit

## Technical Details

- **Framework**: Streamlit
- **Language**: Python 3.11+
- **Dependencies**: streamlit, gspread, google-auth
- **Storage**: Google Sheets integration
- **Session Management**: In-memory (resets on server restart)

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions, please create a GitHub issue with detailed information about your setup and the problem you're experiencing.