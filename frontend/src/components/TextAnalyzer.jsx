import React, { useState } from "react";
import axios from "axios";

const TextAnalyzer = () => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const analyzetext = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", { tncreq: text });
      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing text", error);
      setResult({ error: "Failed to analyze text" });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen w-full flex flex-col bg-gray-900 text-white p-6">
      <div className="flex flex-col items-center justify-center h-[20vh] mt-4 text-center">
  <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500 animate-fadeIn">
    LexiScan
  </h1>
  <h2 className="text-xl md:text-2xl font-medium text-gray-300 mt-2 animate-slideUp">
    Your <span className="text-teal-400 font-semibold">AI-Powered Legal Assistant</span> for Smarter Decisions!
  </h2>
</div>

      {/* Main Content (Scrollable Page) */}
      <div className="w-full max-w-5xl mx-auto space-y-6">
        {/* Input Section */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <textarea
            className="w-full h-40 p-4 border border-gray-600 rounded-md bg-gray-700 text-white resize-none"
            placeholder="Paste Terms & Conditions here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          ></textarea>

          <button
            onClick={analyzetext}
            className="mt-4 w-full bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600 transition"
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {/* Loading Indicator */}
          {loading && (
            <p className="mt-4 text-gray-400 text-center">
              {text.length > 50 ? "Large text detected, processing might take time..." : "Processing..."}
            </p>
          )}
        </div>

        {/* Analysis Result (Doesn't push FAQ down) */}
        {result && (
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold text-blue-300 mb-2">Analysis Result</h2>

            {result.error ? (
              <p className="text-red-500">{result.error}</p>
            ) : (
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold text-blue-200">Summary:</h3>
                  <p className="text-gray-300">{result.Summary || "No summary available"}</p>
                </div>

                <div>
                  <h3 className="font-semibold text-blue-200">Risk Categories:</h3>
                  <ul className="list-disc list-inside text-gray-300">
                    {result.Risk_categories?.length
                      ? result.Risk_categories.map((category, index) => (
                          <li key={index} className="text-yellow-400">{category}</li>
                        ))
                      : <li className="text-gray-400">No major risks detected</li>}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-blue-200">Risk Terms:</h3>
                  <ul className="list-disc list-inside text-gray-300">
                    {result.Risk_terms?.length
                      ? result.Risk_terms.map((term, index) => (
                          <li key={index} className="text-red-400">{term}</li>
                        ))
                      : <li className="text-gray-400">No risky terms found</li>}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-blue-200">Risk Score:</h3>
                  <p className={`text-lg font-bold ${result["Risk score"] > 50 ? "text-red-500" : "text-green-500"}`}>
                    {result["Risk score"] ? result["Risk score"].toFixed(2) : "N/A"}
                  </p>
                </div>

                <div>
                  <h3 className="font-semibold text-blue-200">Final Recommendation:</h3>
                  <p className={`text-lg font-bold ${result.Recommendation?.includes("Not Recommended") ? "text-red-500" : "text-green-500"}`}>
                    {result.Recommendation || "No recommendation available"}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* FAQ Section (Position Fixed, Doesn't Move) */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold text-teal-400 mb-4">Frequently Asked Questions</h2>
          <div className="text-gray-300 space-y-4">
            <div>
              <h3 className="font-semibold text-blue-200">What is LexiScan?</h3>
              <p>LexiScan is an AI-powered Terms & Conditions analyzer designed to help users quickly understand complex legal documents. Using advanced NLP and machine learning, LexiScan extracts key points, highlights potential risks, and provides actionable recommendations—empowering you to make informed decisions with confidence.</p>
            </div>

            <div>
              <h3 className="font-semibold text-blue-200">Why is analyzing Terms & Conditions important?</h3>
              <p>Most users accept Terms & Conditions without reading them. LexiScan helps you understand risks before agreeing.</p>
            </div>

            <div>
              <h3 className="font-semibold text-blue-200">How does LexiScan work?</h3>
              <p>LexiScan uses NLP and machine learning to analyze documents, extract risk terms, and generate summaries with risk scores.</p>
            </div>

            <div>
              <h3 className="font-semibold text-blue-200">Can LexiScan replace legal advice?</h3>
              <p>No, LexiScan is an AI tool for informational purposes. For legal matters, consult a lawyer.</p>
            </div>

            <div>
              <h3 className="font-semibold text-blue-200">Is my data safe?</h3>
              <p>Yes, LexiScan does not store or share your data. All analysis is done securely.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="p-4 w-full text-center bg-gray-900 text-gray-400 mt-6">
        &copy; {new Date().getFullYear()} Rohan Mishra | 
        <a href="https://github.com/romishh3181" className="text-teal-400 ml-1" target="_blank" rel="noopener noreferrer">GitHub</a> |
        <a href="https://www.linkedin.com/in/rohanmishra81" className="text-teal-400 ml-1" target="_blank" rel="noopener noreferrer">LinkedIn</a> |
        <span className="text-teal-400 ml-1">For queries: mavrohan2004@gmail.com</span>
      </footer>
    </div>
  );
};

export default TextAnalyzer;
