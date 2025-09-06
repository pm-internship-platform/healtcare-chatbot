// frontend/js/offline.js
// Service Worker Registration - only register in production/HTTP environment
if ('serviceWorker' in navigator && (window.location.protocol === 'http:' || window.location.protocol === 'https:')) {
    window.addEventListener('load', () => {
        // Register service worker from root path
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
} else {
    console.log('Service Worker not supported in this environment');
}

// Cache for offline responses
const CACHE_NAME = 'health-chatbot-v1';
const OFFLINE_RESPONSES = {
    "What are dengue symptoms?": "Dengue fever typically causes high fever (104°F), severe headache, pain behind eyes, joint and muscle pain, fatigue, nausea, vomiting, and skin rash. In severe cases, it can cause bleeding. If you experience these symptoms, please consult a doctor immediately.",
    "Vaccination schedule for children": "Basic vaccination schedule: \n• Birth: BCG, Hepatitis B-1, OPV-0 \n• 6 weeks: DPT-1, Hepatitis B-2, Hib-1, IPV-1, PCV-1, Rota-1 \n• 10 weeks: DPT-2, Hepatitis B-3, Hib-2, IPV-2, PCV-2, Rota-2 \n• 14 weeks: DPT-3, Hepatitis B-4, Hib-3, IPV-3, PCV-3, Rota-3 \n• 9-12 months: Measles-Rubella-1, JE-1 \n• 16-24 months: DPT booster, Measles-Rubella-2, JE-2, OPV booster",
    "How to prevent malaria?": "Malaria prevention methods: \n1. Use mosquito nets, especially insecticide-treated ones \n2. Apply mosquito repellents on exposed skin \n3. Wear long-sleeved clothing and long pants \n4. Use window and door screens \n5. Eliminate standing water where mosquitoes breed \n6. Take antimalarial medication if prescribed",
    "What are COVID-19 symptoms?": "Common COVID-19 symptoms include fever, dry cough, tiredness, loss of taste or smell, sore throat, headache, and difficulty breathing. If you experience severe symptoms like chest pain or breathing difficulties, seek medical attention immediately.",
    "How to maintain hygiene?": "Good hygiene practices: \n1. Wash hands regularly with soap and water \n2. Use sanitizer when soap is unavailable \n3. Cover mouth when coughing or sneezing \n4. Avoid touching face with unwashed hands \n5. Clean and disinfect frequently touched surfaces \n6. Practice good food hygiene"
};

// Get cached response for offline use
async function getCachedResponse(query) {
    const lowerQuery = query.toLowerCase();
    
    for (const [key, value] of Object.entries(OFFLINE_RESPONSES)) {
        if (lowerQuery.includes(key.toLowerCase().split(' ')[0])) {
            return value;
        }
    }
    
    // Default offline response
    return "I'm currently offline. Here's some general health advice: Maintain good hygiene, drink clean water, eat balanced meals, and consult a doctor for serious health concerns. I'll provide more specific information when I'm back online.";
}

// Cache health information for offline access
async function cacheHealthData() {
    if ('caches' in window && (window.location.protocol === 'http:' || window.location.protocol === 'https:')) {
        try {
            const cache = await caches.open(CACHE_NAME);
            
            // Cache essential health information
            const urlsToCache = [
                '/',
                '/css/tailwind.css',
                '/js/chat.js',
                '/js/quiz.js',
                '/js/offline.js',
                '/assets/bot-avatar.png',
                '/assets/favicon.ico'
            ];
            
            await cache.addAll(urlsToCache);
            console.log('Health data cached for offline use');
        } catch (error) {
            console.log('Caching failed:', error);
        }
    }
}

// Initialize offline functionality
document.addEventListener('DOMContentLoaded', () => {
    // Only cache if we're in a proper HTTP environment
    if (window.location.protocol === 'http:' || window.location.protocol === 'https:') {
        cacheHealthData();
        
        // Periodically check connection and update cache
        setInterval(() => {
            if (navigator.onLine) {
                cacheHealthData();
            }
        }, 3600000); // Update cache every hour when online
    }
});