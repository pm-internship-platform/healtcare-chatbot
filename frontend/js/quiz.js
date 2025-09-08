const quizBtn = document.getElementById('quiz-btn');
const quizModal = document.getElementById('quiz-modal');
const closeQuiz = document.getElementById('close-quiz');
const quizContent = document.getElementById('quiz-content');
const nextQuestion = document.getElementById('next-question');

let currentQuiz = null;
let currentQuestionIndex = 0;
let score = 0;

const sampleQuiz = {
    title: "General Health Knowledge",
    questions: [
        {
            question: "What is the primary symptom of dengue fever?",
            options: [
                "High fever and severe headache",
                "Cough and cold",
                "Joint pain and swelling",
                "Skin rashes only"
            ],
            correctAnswer: 0
        },
        {
            question: "How can malaria be prevented?",
            options: [
                "Using mosquito nets",
                "Drinking boiled water",
                "Washing hands regularly",
                "Avoiding crowded places"
            ],
            correctAnswer: 0
        },
        {
            question: "At what age should a child receive the measles vaccine?",
            options: [
                "At birth",
                "6 months",
                "9 months",
                "1 year"
            ],
            correctAnswer: 2
        }
    ]
};

quizBtn.addEventListener('click', () => {
    startQuiz();
    quizModal.classList.remove('hidden');
});

closeQuiz.addEventListener('click', () => {
    quizModal.classList.add('hidden');
    resetQuiz();
});

function startQuiz() {
    currentQuiz = sampleQuiz;
    currentQuestionIndex = 0;
    score = 0;
    loadQuestion(currentQuestionIndex);
}

function loadQuestion(index) {
    if (!currentQuiz || index >= currentQuiz.questions.length) {
        showQuizResults();
        return;
    }
    
    const question = currentQuiz.questions[index];
    quizContent.innerHTML = `
        <h4 class="font-medium mb-4">${question.question}</h4>
        <div class="space-y-2">
            ${question.options.map((option, i) => `
                <button class="quiz-option w-full text-left p-3 border border-gray-300 rounded-lg hover:bg-gray-50" data-index="${i}">
                    ${option}
                </button>
            `).join('')}
        </div>
    `;
    
    document.querySelectorAll('.quiz-option').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const selectedIndex = parseInt(e.target.getAttribute('data-index'));
            checkAnswer(selectedIndex);
        });
    });
    
    nextQuestion.classList.add('hidden');
}

function checkAnswer(selectedIndex) {
    const correctIndex = currentQuiz.questions[currentQuestionIndex].correctAnswer;
    const options = document.querySelectorAll('.quiz-option');
    
    options.forEach(btn => {
        btn.disabled = true;
    });
    
    options[correctIndex].classList.add('bg-green-100', 'border-green-500');
    
    if (selectedIndex !== correctIndex) {
        options[selectedIndex].classList.add('bg-red-100', 'border-red-500');
    } else {
        score++;
    }
    
    nextQuestion.classList.remove('hidden');
}

function showQuizResults() {
    quizContent.innerHTML = `
        <div class="text-center py-4">
            <h4 class="font-bold text-lg mb-2">Quiz Completed!</h4>
            <p class="text-gray-700">Your score: ${score} out of ${currentQuiz.questions.length}</p>
            <div class="my-6">
                <p class="text-sm text-gray-600">Share your achievement:</p>
                <div class="flex justify-center space-x-4 mt-2">
                    <button class="p-2 bg-blue-100 text-blue-600 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    nextQuestion.classList.add('hidden');
}

function resetQuiz() {
    currentQuiz = null;
    currentQuestionIndex = 0;
    score = 0;
}

nextQuestion.addEventListener('click', () => {
    currentQuestionIndex++;
    loadQuestion(currentQuestionIndex);
});