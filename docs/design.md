# High-Level Design: Quantitative Strategy Input Page

This document describes the high-level design and architecture of the Quantitative Strategy Input Page.

## 1. Overview

The application is a single-page web application built with HTML, CSS, and JavaScript. It allows users to input details about a financial asset and a quantitative trading strategy, then submit this information.

The core components are:
- **`indexcoin.html`**: Defines the structure and content of the web page.
- **`stylecoin.css`**: Provides the visual styling for the page elements.
- **`scriptcoin.js`**: Implements the client-side logic, interactivity, and data handling.

## 2. Component Breakdown

### 2.1. `indexcoin.html` (HTML Structure)

- **Purpose**: To lay out the user interface elements.
- **Key Sections**:
    - **Header**: Title of the page.
    - **Asset Input Section**:
        - A `label` for the asset input field.
        - An `input type="text"` field (`id="asset-input"`) for the user to enter the stock code, crypto symbol, or blockchain address.
    - **Existing Strategy Section**:
        - A `label` for the strategy selection.
        - A `select` dropdown menu (`id="existing-strategy-select"`) for choosing from a list of predefined strategies. Options are populated by JavaScript.
    - **Custom Strategy Section**:
        - A `label` for the custom strategy input.
        - A `textarea` (`id="custom-strategy-input"`) for the user to type their custom strategy.
    - **Submission Section**:
        - A `button` (`id="submit-button"`) to trigger the data submission process.
- **Dependencies**:
    - Links to `stylecoin.css` for styling.
    - Links to `scriptcoin.js` for functionality (placed before the closing `</body>` tag).

### 2.2. `stylecoin.css` (Styling)

- **Purpose**: To enhance the visual appearance and usability of the page.
- **Key Styling Aspects**:
    - **Global Styles**: Basic body styling, font choices, background color.
    - **Container**: Centered content area with padding and shadow for a card-like effect.
    - **Headings**: Styling for `<h1>` and `<h2>` elements.
    - **Input Fields**: Consistent styling for `input[type="text"]`, `select`, and `textarea`, including focus states.
    - **Button**: Styling for the submit button, including hover and active states.
    - **Layout**: Uses flexbox for centering the main container.
    - **Responsiveness**: Basic media query for adjusting layout on smaller screens.

### 2.3. `scriptcoin.js` (Client-Side Logic)

- **Purpose**: To handle user interactions, data manipulation, and communication (currently console logging).
- **Key Functionalities**:
    - **DOMContentLoaded Listener**: Ensures the script runs after the HTML is fully loaded.
    - **Element Selection**: Retrieves references to key HTML elements (input fields, select, textarea, button).
    - **Mock Strategy Population**:
        - Defines an array of mock strategy objects (e.g., `{ id: 'strategy1', name: 'Moving Average Crossover' }`).
        - Dynamically creates `option` elements and appends them to the `existing-strategy-select` dropdown.
    - **Event Handling for Mutual Exclusivity**:
        - An event listener on `existing-strategy-select` clears `custom-strategy-input` when a selection is made.
        - An event listener on `custom-strategy-input` clears the selection in `existing-strategy-select` when text is input.
    - **Submit Button Event Listener**:
        - Attached to the `submit-button`.
        - **Data Collection**: Retrieves values from `asset-input`, `existing-strategy-select`, and `custom-strategy-input`.
        - **Input Validation**:
            - Checks if the asset input is empty. If so, shows an alert and focuses the field.
            - Checks if neither an existing strategy is selected nor a custom strategy is provided. If so, shows an alert.
        - **Data Structuring**: Creates an object containing the asset, strategy details (type, id/name or text), and a timestamp.
        - **Output**: Logs the structured data to the browser's console using `console.log()`. Shows an alert to the user confirming submission.
- **Data Flow on Submission**:
    1. User clicks the "Submit" button.
    2. The JavaScript event listener is triggered.
    3. Values are read from the input fields.
    4. Basic validation is performed.
    5. If valid, data is packaged into a JavaScript object.
    6. The object is logged to the browser's console.

## 3. Interaction Diagram (Simplified)

```
User Interface (indexcoin.html) <--- Styles (stylecoin.css)
      |
      | User Interaction (e.g., input, select, click)
      v
JavaScript Logic (scriptcoin.js)
      |
      | DOM Manipulation (e.g., populate dropdown, clear fields)
      | Data Processing & Validation
      v
Browser Console (Output for submitted data)
```

This design provides a clear separation of concerns: structure (HTML), presentation (CSS), and behavior (JavaScript), making the application modular and easier to maintain.
