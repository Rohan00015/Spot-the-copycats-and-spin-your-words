document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("plagiarismForm");
    const resultSection = document.getElementById("resultSection");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Clear previous results
        resultSection.style.display = "none";
        document.getElementById("plagiarismPercentage").textContent = '';
        document.getElementById("uniquePercentage").textContent = '';
        document.getElementById("plagiarizedList").innerHTML = '';
        document.getElementById("rewrittenList").innerHTML = '';

        const textInput = document.getElementById("textInput").value.trim();
        if (!textInput) {
            alert("Please enter some text to check for plagiarism.");
            return;
        }

        // Show loading animation
        form.querySelector("button").textContent = "Checking...";
        form.querySelector("button").disabled = true;

        try {
            // Send AJAX request to the server
            const response = await fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ text: textInput }),
            });

            if (!response.ok) throw new Error("Something went wrong. Please try again later.");

            const result = await response.json();

            // Populate results
            document.getElementById("plagiarismPercentage").textContent = result.plagiarism_percentage.toFixed(2);
            document.getElementById("uniquePercentage").textContent = result.unique_percentage.toFixed(2);

            const plagiarizedList = document.getElementById("plagiarizedList");
            const rewrittenList = document.getElementById("rewrittenList");

            plagiarizedList.innerHTML = result.plagiarized_sentences.map(s => `<li>${s}</li>`).join('');
            rewrittenList.innerHTML = result.rewritten_sentences.map(s => `<li>${s}</li>`).join('');

            // Show result section
            resultSection.style.display = "block";
            resultSection.scrollIntoView({ behavior: "smooth" });

        } catch (error) {
            alert(error.message);
        } finally {
            // Reset button state
            form.querySelector("button").textContent = "Check for Plagiarism";
            form.querySelector("button").disabled = false;
        }
    });
});
