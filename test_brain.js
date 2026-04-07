const brain = require("brain.js");

try {
    const strategyNet = new brain.NeuralNetwork({ hiddenLayers: [6] });

    strategyNet.train([
        { input: { avg: 0.20, att: 0.30 }, output: { profile1: 1 } },
        { input: { avg: 0.40, att: 0.85 }, output: { profile2: 1 } },
        { input: { avg: 0.50, att: 0.60 }, output: { profile3: 1 } },
        { input: { avg: 0.65, att: 0.85 }, output: { profile4: 1 } },
        { input: { avg: 0.70, att: 0.75 }, output: { profile5: 1 } },
        { input: { avg: 0.85, att: 0.50 }, output: { profile6: 1 } },
        { input: { avg: 0.90, att: 0.90 }, output: { profile7: 1 } },
        { input: { avg: 0.98, att: 0.95 }, output: { profile8: 1 } }
    ]);
    console.log("NeuralNetwork trained");

    const nlpNet = new brain.recurrent.LSTM();
    nlpNet.train([
        { input: "hello", output: "greeting" },
        { input: "hi there", output: "greeting" },
        { input: "help me", output: "help" },
        { input: "how to use", output: "help" },
        { input: "student marks", output: "analysis" },
        { input: "attendance and marks", output: "analysis" },
        { input: "85 90", output: "analysis" }
    ], { iterations: 100 });
    console.log("LSTM trained");
} catch (e) {
    console.error(e);
}
