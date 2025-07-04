document.addEventListener('DOMContentLoaded', function () {
    // Re-define detailedStrategies (in a real app, this would come from a shared source or API)
    const detailedStrategies = [
        {
            id: 'momentum-trading',
            name: 'Momentum Trading',
            description: 'Capitalizes on the continuance of existing market trends. It involves buying assets that have shown an upward trend and selling those that have shown a downward trend. This approach assumes that an asset price that has been rising will continue to rise, and vice versa.',
            score: 80,
            likes: 125,
            details: {
                suitableScenarios: 'Trending markets (bull or bear), volatile assets with clear directional movement. Less effective in sideways or range-bound markets.',
                formula: '1. Identify Trend: Use indicators like Moving Averages (e.g., price > 50-day MA), ADX (>25 indicates trend strength).\n2. Entry Signal: Buy when price breaks above a recent high or a key resistance level in an uptrend. Sell/Short when price breaks below a recent low or support in a downtrend.\n3. Confirmation: Volume should ideally increase in the direction of the breakout.\n4. Stop Loss: Place a stop-loss below the recent swing low (for buys) or above the recent swing high (for shorts).\n5. Take Profit: Can be a fixed risk/reward ratio (e.g., 2:1 or 3:1), a trailing stop, or when signs of trend exhaustion appear.',
                successRate: '60-75% in strongly trending conditions. Success is highly dependent on correctly identifying the trend and managing risk.',
                historicalComments: [
                    { user: 'TraderX', comment: 'Worked well for me during the last bull run on tech stocks.' },
                    { user: 'AnalystY', comment: 'Requires careful risk management and discipline. Whipsaws can be costly in choppy markets.' },
                    { user: 'MomentumKing', comment: 'Best when combined with volume analysis.'}
                ]
            }
        },
        {
            id: 'mean-reversion',
            name: 'Mean Reversion',
            description: 'Based on the theory that asset prices and historical returns eventually revert to their long-run mean or average level. This strategy profits by taking positions that bet on prices returning to their historical average.',
            score: 70,
            likes: 98,
            details: {
                suitableScenarios: 'Range-bound markets, stable assets (e.g., some blue-chip stocks, currency pairs in certain conditions), assets with predictable volatility cycles. Not suitable for assets in strong, sustained trends.',
                formula: '1. Identify Mean: Calculate a moving average (e.g., 20-period SMA) or use Bollinger Bands.\n2. Identify Extremes: Buy when price drops significantly below the mean (e.g., touches lower Bollinger Band, or RSI < 30). Sell/Short when price rises significantly above the mean (e.g., touches upper Bollinger Band, or RSI > 70).\n3. Confirmation: Look for candlestick reversal patterns or divergence on oscillators.\n4. Stop Loss: Place beyond the recent extreme or a fixed percentage from entry.\n5. Take Profit: Target the moving average or the opposite Bollinger Band.',
                successRate: '55-70% in non-trending, volatile markets. Profit per trade is often smaller than momentum strategies, requiring higher win rates.',
                historicalComments: [
                    { user: 'QuantMaster', comment: 'Good for pair trading (e.g., two correlated stocks) or stable large-cap stocks.' },
                    { user: 'NewbieZ', comment: 'Hard to time the exact reversal point. Sometimes it keeps going!' },
                    { user: 'BandsFan', comment: 'Bollinger Bands are my go-to for this.'}
                ]
            }
        },
        {
            id: 'arbitrage-opportunities',
            name: 'Arbitrage Opportunities',
            description: 'Exploits tiny price differences of identical assets in different markets or forms. This strategy involves simultaneously buying and selling the asset to lock in a risk-free profit. It is often low-risk but requires speed, capital, and low transaction costs.',
            score: 90,
            likes: 210,
            details: {
                suitableScenarios: 'Liquid assets listed on multiple exchanges (e.g., large cryptocurrencies, inter-listed stocks), inefficiencies in market pricing, during mergers & acquisitions (risk arbitrage).',
                formula: '1. Identify Discrepancy: Monitor prices of the same asset across different venues.\n2. Condition: Price(Venue B) - Price(Venue A) > Transaction_Costs_A + Transaction_Costs_B.\n3. Execution: Simultaneously buy on Venue A and sell on Venue B.\n4. Automation: Often requires automated trading systems (bots) due to the fleeting nature of opportunities.',
                successRate: 'High (>90%) for pure arbitrage when an opportunity is correctly identified and executed instantly. Opportunities are rare and often competed away quickly.',
                historicalComments: [
                    { user: 'SpeedyBot', comment: 'Execution speed and low latency are absolutely key. Manual arbitrage is nearly impossible now.' },
                    { user: 'RegulatorWatch', comment: 'Ensure compliance with all market rules and regulations. Some forms might be restricted.' },
                    { user: 'FeeWatcher', comment: 'Transaction fees can eat up all the profit if not careful.'}
                ]
            }
        },
        {
            id: 'ai-sentiment-analysis',
            name: 'AI-Powered Sentiment Analysis',
            description: 'Uses natural language processing (NLP) and machine learning (ML) to analyze market sentiment from news articles, social media posts, financial reports, and other text sources to predict potential price movements.',
            score: 85,
            likes: 150,
            details: {
                suitableScenarios: 'Assets heavily influenced by news and public opinion (e.g., meme stocks, specific sectors like biotech), event-driven trading, short to medium-term predictions.',
                formula: '1. Data Collection: Aggregate text data from various sources (Twitter, news APIs, Reddit, etc.).\n2. Sentiment Scoring: Use NLP models (e.g., BERT, VADER) to classify text as positive, negative, or neutral and assign a sentiment score.\n3. Signal Generation: If aggregate sentiment score for an asset crosses a certain positive threshold, generate a buy signal. If it crosses a negative threshold, generate a sell signal.\n4. Integration: Combine with other technical or fundamental indicators for confirmation.\n5. Model Maintenance: Continuously monitor and retrain the ML model as language and sentiment expression evolve.',
                successRate: 'Varies widely (50-70%) depending on model accuracy, data quality, and market regime. Highly empirical.',
                historicalComments: [
                    { user: 'DataScientist', comment: 'The model needs constant retraining and feature engineering. Garbage in, garbage out.' },
                    { user: 'NewsJunkie', comment: 'Fascinating to see how collective emotion sways markets. But it\'s not a crystal ball.' },
                    { user: 'EthicalAI', comment: 'Important to consider biases in data and algorithms.'}
                ]
            }
        }
    ];

    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    const strategyId = getQueryParam('id');
    const strategy = detailedStrategies.find(s => s.id === strategyId);

    if (strategy) {
        document.title = strategy.name + " - Details"; // Update page title
        document.getElementById('strategy-name').textContent = strategy.name;
        document.getElementById('strategy-description').textContent = strategy.details.description || strategy.description; // Use detailed description if available
        document.getElementById('strategy-suitable-scenarios').textContent = strategy.details.suitableScenarios;
        document.getElementById('strategy-formula').textContent = strategy.details.formula;
        document.getElementById('strategy-success-rate').textContent = strategy.details.successRate;

        const commentsList = document.getElementById('strategy-historical-comments');
        commentsList.innerHTML = ''; // Clear loading/default message
        if (strategy.details.historicalComments && strategy.details.historicalComments.length > 0) {
            strategy.details.historicalComments.forEach(comment => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<strong>${comment.user}:</strong> ${comment.comment}`;
                commentsList.appendChild(listItem);
            });
        } else {
            commentsList.innerHTML = '<li>No comments available.</li>';
        }
    } else {
        const container = document.querySelector('.strategy-detail-container');
        if (container) {
            container.innerHTML = `<h1>Strategy Not Found</h1><p>The requested strategy ID "${strategyId}" could not be found.</p><a href="indexcoin.html" class="back-link">&laquo; Back to Main Page</a>`;
        }
    }
});
