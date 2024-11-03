document.addEventListener("DOMContentLoaded", function() {
    // Apply a fade-in and slide-up effect to messages
    const messageContainer = document.querySelectorAll('.message');
    messageContainer.forEach((message, index) => {
        message.style.opacity = 0;
        message.style.transform = "translateY(20px)";
        setTimeout(() => {
            message.style.opacity = 1;
            message.style.transform = "translateY(0)";
            message.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        }, index * 100); // Staggered effect for each message
    });

    // Custom welcome message display animation
    const welcomeMessage = document.getElementById("welcome-message");
    if (welcomeMessage) {
        welcomeMessage.style.opacity = 0;
        setTimeout(() => {
            welcomeMessage.style.opacity = 1;
            welcomeMessage.style.transition = "opacity 1s ease-in-out";
        }, 500); // Delay before showing the welcome message
    }

    // Smooth scroll to the latest message with a delay
    function scrollToBottom() {
        const chatHistory = document.querySelector(".chat-history");
        if (chatHistory) {
            setTimeout(() => {
                chatHistory.scrollTo({ top: chatHistory.scrollHeight, behavior: 'smooth' });
            }, 100); // Small delay to ensure new messages are rendered
        }
    }

    // Observe for new messages and scroll to the latest
    const chatContainer = document.querySelector(".chat-history");
    if (chatContainer) {
        const observer = new MutationObserver(scrollToBottom);
        observer.observe(chatContainer, { childList: true });

        // Disconnect observer on page unload to improve performance
        window.addEventListener("beforeunload", () => observer.disconnect());
    }

    // Theme toggle functionality with visual feedback on button
    const toggleThemeButton = document.getElementById("toggle-theme");
    if (toggleThemeButton) {
        toggleThemeButton.addEventListener("click", () => {
            document.body.classList.toggle("dark-theme");
            const isDark = document.body.classList.contains("dark-theme");
            localStorage.setItem("theme", isDark ? "dark" : "light");
            toggleThemeButton.textContent = isDark ? "Switch to Light Mode" : "Switch to Dark Mode";
        });
    }

    // Apply saved theme preference and update toggle button text
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        document.body.classList.add(savedTheme);
        if (toggleThemeButton) {
            toggleThemeButton.textContent = savedTheme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode";
        }
    }
});
