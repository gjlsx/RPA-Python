document.addEventListener('DOMContentLoaded', function() {
    const assetInput = document.getElementById('asset-input');
    const existingStrategySelect = document.getElementById('existing-strategy-select');
    const customStrategyInput = document.getElementById('custom-strategy-input');
    const submitButton = document.getElementById('submit-button');

    // Mock data for existing strategies
    const mockStrategies = [
        { id: 'strategy1', name: 'Moving Average Crossover' },
        { id: 'strategy2', name: 'RSI Overbought/Oversold' },
        { id: 'strategy3', name: 'Bollinger Bands Squeeze' },
        { id: 'strategy4', name: 'MACD Signal Line Crossover' }
    ];

    // Populate existing strategies dropdown
    mockStrategies.forEach(strategy => {
        const option = document.createElement('option');
        option.value = strategy.id;
        option.textContent = strategy.name;
        existingStrategySelect.appendChild(option);
    });

    // Handle form submission
    submitButton.addEventListener('click', function() {
        const asset = assetInput.value.trim();
        const selectedStrategyId = existingStrategySelect.value;
        const customStrategy = customStrategyInput.value.trim();

        if (!asset) {
            alert('Please enter a stock/crypto code or address.');
            assetInput.focus();
            return;
        }

        let strategyDetails = {};

        if (selectedStrategyId) {
            const selectedStrategy = mockStrategies.find(s => s.id === selectedStrategyId);
            strategyDetails = {
                type: 'existing',
                id: selectedStrategyId,
                name: selectedStrategy ? selectedStrategy.name : 'Unknown Strategy'
            };
            // Clear custom strategy if an existing one is selected
            customStrategyInput.value = '';
        } else if (customStrategy) {
            strategyDetails = {
                type: 'custom',
                text: customStrategy
            };
             // Clear selected strategy if a custom one is input
            existingStrategySelect.value = '';
        } else {
            alert('Please select an existing strategy or input a custom strategy.');
            return;
        }

        const submissionData = {
            asset: asset,
            strategy: strategyDetails,
            timestamp: new Date().toISOString()
        };

        // For now, just log the data to the console
        console.log('Form Submitted:', submissionData);
        alert('Form submitted! Check the console for the data.');

        // Optionally, clear fields after submission
        // assetInput.value = '';
        // existingStrategySelect.value = '';
        // customStrategyInput.value = '';
    });

    // Logic to ensure only one strategy type is primarily selected/filled
    existingStrategySelect.addEventListener('change', function() {
        if (this.value !== '') {
            customStrategyInput.value = ''; // Clear custom input if existing is chosen
        }
    });

    customStrategyInput.addEventListener('input', function() {
        if (this.value.trim() !== '') {
            existingStrategySelect.value = ''; // Clear existing selection if custom is typed
        }
    });
});
