// Test the ML chatbot integration
async function testMLChatbot() {
    console.log('🧪 Testing ML Chatbot Integration...');
    
    const testMessages = [
        "Hello, I'm looking for an engagement ring",
        "What materials do you recommend?",
        "How much does a diamond ring cost?",
        "Tell me about your bespoke process"
    ];
    
    for (let i = 0; i < testMessages.length; i++) {
        const message = testMessages[i];
        console.log(`\n${i + 1}. Testing: "${message}"`);
        
        try {
            const response = await fetch('http://localhost:3001/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            const text = await response.text();
            console.log('Response:', text.substring(0, 200) + '...');
            
        } catch (error) {
            console.error('Error:', error.message);
        }
    }
    
    console.log('\n✅ ML Chatbot integration test completed!');
}

testMLChatbot();