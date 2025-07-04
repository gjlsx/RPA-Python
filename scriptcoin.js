document.addEventListener('DOMContentLoaded', function() {
    const assetInput = document.getElementById('asset-input');
    const existingStrategySelect = document.getElementById('existing-strategy-select');
    const customStrategyInput = document.getElementById('custom-strategy-input');
    const submitButton = document.getElementById('submit-button');
    const recommendationsSection = document.querySelector('.recommendations-section'); // Get the section for recommendations

    // Enhanced mock data for strategies
    const detailedStrategies = [
        {
            id: 'momentum-trading',
            name: 'Momentum Trading',
            description: 'Capitalizes on the continuance of existing market trends. It involves buying assets that have shown an upward trend and selling those that have shown a downward trend.',
            score: 80, // Score out of 100
            likes: 125,
            details: {
                suitableScenarios: 'Trending markets, volatile assets with clear directional movement.',
                formula: 'Buy when Price > N-day Moving Average and N-day Price Change > X%. Sell when Price < N-day Moving Average or target profit/stop loss hit.',
                successRate: '60-75% in strongly trending conditions.',
                historicalComments: [
                    { user: 'TraderX', comment: 'Worked well for me during the last bull run.' },
                    { user: 'AnalystY', comment: 'Requires careful risk management.' }
                ]
            }
        },
        {
            id: 'mean-reversion',
            name: 'Mean Reversion',
            description: 'Based on the theory that asset prices and historical returns eventually revert to their long-run mean or average level.',
            score: 70, // Score out of 100
            likes: 98,
            details: {
                suitableScenarios: 'Range-bound markets, stable assets, assets with predictable volatility cycles.',
                formula: 'Buy when price drops X standard deviations below mean, sell when it rises Y standard deviations above mean or reverts to mean.',
                successRate: '55-70% in non-trending, volatile markets.',
                historicalComments: [
                    { user: 'QuantMaster', comment: 'Good for pair trading or stable stocks.' },
                    { user: 'NewbieZ', comment: 'Hard to time the exact reversal point.' }
                ]
            }
        },
        {
            id: 'arbitrage-opportunities',
            name: 'Arbitrage Opportunities',
            description: 'Exploits price differences of identical assets in different markets. This strategy is often low-risk but requires speed and volume.',
            score: 90, // Score out of 100
            likes: 210,
            details: {
                suitableScenarios: 'Liquid assets listed on multiple exchanges, inefficiencies in market pricing.',
                formula: 'Simultaneously buy asset on Exchange A at Price X and sell on Exchange B at Price Y, where Y > X + transaction_costs.',
                successRate: 'High (>90%) when an opportunity is correctly identified and executed quickly, but opportunities are rare.',
                historicalComments: [
                    { user: 'SpeedyBot', comment: 'Execution speed is key.' },
                    { user: 'RegulatorWatch', comment: 'Ensure compliance with all market rules.' }
                ]
            }
        },
        {
            id: 'ai-sentiment-analysis',
            name: 'AI-Powered Sentiment Analysis',
            description: 'Uses natural language processing and machine learning to analyze market sentiment from news, social media, and reports to predict price movements.',
            score: 85, // Score out of 100
            likes: 150,
            details: {
                suitableScenarios: 'Assets heavily influenced by news and public opinion, event-driven trading.',
                formula: 'Generate buy/sell signals based on aggregated sentiment scores (e.g., positive, negative, neutral) derived from text data sources.',
                successRate: 'Varies widely (50-70%) depending on model accuracy and data quality.',
                historicalComments: [
                    { user: 'DataScientist', comment: 'Model needs constant retraining.' },
                    { user: 'NewsJunkie', comment: 'Fascinating to see how news moves markets.' }
                ]
            }
        }
    ];

    // Populate existing strategies dropdown
    detailedStrategies.forEach(strategy => {
        const option = document.createElement('option');
        option.value = strategy.id;
        option.textContent = strategy.name;
        existingStrategySelect.appendChild(option);
    });

    // Populate Recommended Strategies Section
    function populateRecommendations() {
        // Clear existing recommendations (if any, e.g., static ones or from previous population)
        // Find the H2 inside recommendationsSection and clear siblings after it.
        const heading = recommendationsSection.querySelector('h2');
        while (heading && heading.nextSibling) {
            recommendationsSection.removeChild(heading.nextSibling);
        }

        detailedStrategies.forEach(strategy => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';

            const nameLink = document.createElement('a');
            nameLink.href = `strategy_detail.html?id=${strategy.id}`; // Placeholder link
            nameLink.className = 'recommendation-name-link';
            nameLink.textContent = strategy.name;

            const title = document.createElement('h3');
            title.appendChild(nameLink);

            const description = document.createElement('p');
            description.textContent = strategy.description;

            const score = document.createElement('p');
            score.className = 'score';
            score.textContent = `Score: ${strategy.score}/100`;

            const likes = document.createElement('p');
            likes.className = 'likes';
            // Simple like icon (could be replaced with SVG or font icon)
            likes.innerHTML = `❤️ ${strategy.likes} Likes`;

            item.appendChild(title);
            item.appendChild(description);
            item.appendChild(score);
            item.appendChild(likes);
            recommendationsSection.appendChild(item);
        });
    }

    if (recommendationsSection) {
        populateRecommendations();
    }

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
            const selectedStrategy = detailedStrategies.find(s => s.id === selectedStrategyId);
            strategyDetails = {
                type: 'existing',
                id: selectedStrategyId,
                name: selectedStrategy ? selectedStrategy.name : 'Unknown Strategy'
                // Potentially add more details from selectedStrategy if needed for submission
            };
            customStrategyInput.value = ''; // Clear custom strategy
        } else if (customStrategy) {
            strategyDetails = {
                type: 'custom',
                text: customStrategy
            };
            existingStrategySelect.value = ''; // Clear selected strategy
        } else {
            alert('Please select an existing strategy or input a custom strategy.');
            return;
        }

        const submissionData = {
            asset: asset,
            strategy: strategyDetails,
            timestamp: new Date().toISOString()
        };

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
