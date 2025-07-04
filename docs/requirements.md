# Requirements Specification: Quantitative Strategy Input Page

This document outlines the requirements for the Quantitative Strategy Input Page.

## 1. Functional Requirements

### 1.1. Asset Input
- The user shall be able to input an identifier for a financial asset. This can be a stock ticker (e.g., AAPL), a cryptocurrency symbol (e.g., BTC), or a blockchain address (e.g., 0x...).
- There shall be a dedicated input field for this purpose.

### 1.2. Strategy Selection/Input
- **Existing Strategies:**
    - The user shall be able to select a quantitative strategy from a predefined list of existing strategies.
    - This selection shall be made using a dropdown menu.
- **Custom Strategy:**
    - The user shall be able to input their own quantitative strategy as text.
    - There shall be a multi-line text area for this purpose.
- **Mutual Exclusivity:**
    - If an existing strategy is selected, any text in the custom strategy input should ideally be cleared or ignored upon submission.
    - If text is entered into the custom strategy input, any selected existing strategy should ideally be deselected or ignored upon submission. The system should prioritize one over the other if both are somehow provided (e.g., prioritize custom if filled, otherwise existing if selected).

### 1.3. Submission
- The user shall be able to submit the entered asset identifier and the chosen/defined strategy.
- There shall be a dedicated submit button.
- Upon submission, the system should collect:
    - The asset identifier.
    - The selected existing strategy (if chosen) OR the custom strategy text (if input).
    - A timestamp of the submission.
- Initially, the submitted data will be logged to the browser's console.

### 1.4. Validation
- The system shall validate that an asset identifier has been provided before submission.
- The system shall validate that either an existing strategy has been selected OR a custom strategy has been input before submission. An alert or message should inform the user if these conditions are not met.

## 2. Non-Functional Requirements

### 2.1. User Interface
- The application shall be a single HTML page.
- The interface should be clean, intuitive, and easy to use.
- Basic styling should be applied for good visual presentation.

### 2.2. Filename Convention
- All primary source files (HTML, CSS, JavaScript) shall be prefixed with "coin" as per user request (e.g., `indexcoin.html`, `stylecoin.css`, `scriptcoin.js`).

### 2.3. Technology
- The frontend shall be built using HTML, CSS, and vanilla JavaScript. No external frameworks or libraries are required for the core functionality at this stage.

## 3. Future Considerations (Out of Scope for Initial Version)
- Storing submitted data persistently (e.g., in a database).
- More sophisticated validation of asset identifiers or strategy text.
- User authentication.
- Dynamic loading of existing strategies from a server.
- Actual execution or backtesting of strategies.
