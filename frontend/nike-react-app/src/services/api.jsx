const BASE_URL = "http://localhost:8000"; // Adjust if needed

export async function fetchRecommendations(prompt) {
    const response = await fetch(`${BASE_URL}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
    });

    if (!response.ok) throw new Error("Failed to fetch recommendations");

    return await response.json();
}
