import { useState } from "react";
import "./App.css";

function App() {
  const [gameState, setGameState] = useState("START"); // START, PLAYING, WON, LOST
  const [loading, setLoading] = useState(false);
  const [caseFile, setCaseFile] = useState(null);

  // Player state tracking
  const [cluesFound, setCluesFound] = useState([]);
  const [interrogatedSuspects, setInterrogatedSuspects] = useState([]);
  const [score, setScore] = useState(0);
  const [interrogationCount, setInterrogationCount] = useState(0);
  const maxInterrogations = 5;

  // UI Selection states
  const [activeSuspectId, setActiveSuspectId] = useState(null);
  const [systemMessage, setSystemMessage] = useState(
    "Awaiting assignment, Detective.",
  );

  // Start a fresh AI Case
  const startNewGame = async () => {
    setLoading(true);
    setSystemMessage("Connecting to mainframe... Generating Case File...");
    try {
      const response = await fetch("http://127.0.0.1:5000/api/new-game");
      const data = await response.json();
      if (data.error) throw new Error(data.error);

      setCaseFile(data);
      setCluesFound([]);
      setInterrogatedSuspects([]);
      setScore(0);
      setInterrogationCount(0);
      setActiveSuspectId(null);
      setGameState("PLAYING");
      setSystemMessage(
        "Case profile generated. Review the report and begin interrogation.",
      );
    } catch (err) {
      setSystemMessage(`Error accessing database: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Interrogate a suspect (Client-side logic)
  const interrogateSuspect = (suspect) => {
    // 1. Check if we're out of total allowed interrogations
    if (
      interrogationCount >= maxInterrogations &&
      !interrogatedSuspects.includes(suspect.id)
    ) {
      setSystemMessage(
        "CRITICAL: Out of interrogation warrants! You must make an accusation.",
      );
      return;
    }

    setActiveSuspectId(suspect.id);

    // 2. Count how many times we've already poked THIS specific suspect
    const timesInterrogated = interrogatedSuspects.filter(
      (id) => id === suspect.id,
    ).length;

    // 3. If they still have remaining hidden clues, give them EXACTLY ONE new clue
    if (timesInterrogated < suspect.clues.length) {
      const nextClue = suspect.clues[timesInterrogated];

      if (!cluesFound.includes(nextClue)) {
        setCluesFound((prev) => [...prev, nextClue]);
        setInterrogationCount((prev) => prev + 1);
        setInterrogatedSuspects((prev) => [...prev, suspect.id]);
        setSystemMessage(
          `Interrogating ${suspect.name}. Breakthrough achieved: New clue logged into profile.`,
        );
      }
    } else {
      setSystemMessage(
        `Re-examining details for ${suspect.name}. They have nothing left to say.`,
      );
    }
  };

  // Scan collected clues for contradictions
  const checkContradictions = () => {
    if (!caseFile) return;
    let pointsEarned = 0;
    let foundAny = false;

    caseFile.suspects.forEach((suspect) => {
      // If the player has uncovered the specific broken clue matching this suspect's contradiction
      if (cluesFound.includes(suspect.contradiction.clue)) {
        // Simple trick: stash points directly on the clue text to avoid awarding it twice
        if (
          !cluesFound.includes(
            `[PROVEN LIE] ${suspect.contradiction.explanation}`,
          )
        ) {
          pointsEarned += suspect.contradiction.points;
          foundAny = true;
          setCluesFound((prev) => [
            ...prev,
            `[PROVEN LIE] ${suspect.contradiction.explanation}`,
          ]);
        }
      }
    });

    if (foundAny) {
      setScore((prev) => prev + pointsEarned);
      setSystemMessage(
        `ALIBI CRACKED: Alibi inconsistencies mapped! Awarded +${pointsEarned} points.`,
      );
    } else {
      setSystemMessage(
        "ANALYSIS COMPLETE: No active contradictions discovered in your current evidence archive.",
      );
    }
  };

  // Submit final choice to secure verification API
  const handleAccuse = async (suspectId) => {
    setSystemMessage("Transmitting warrant data to server...");
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/verify-accusation",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            accused_id: suspectId,
            thief_id: caseFile.thief_id,
          }),
        },
      );
      const result = await response.json();

      if (result.correct) {
        setScore((prev) => prev + result.bonus_points);
        setGameState("WON");
        setSystemMessage(result.message);
      } else {
        setScore((prev) => prev - 25);
        // setScore((prev) => Math.max(0, prev - 25));
        setSystemMessage(`❌ WRONG ACCUSATION: ${result.message} (-25 pts)`);
      }
    } catch (err) {
      console.log(err);
      setSystemMessage("Communication failure during server confirmation.");
    }
  };

  const selectedSuspect = caseFile?.suspects.find(
    (s) => s.id === activeSuspectId,
  );

  return (
    <div className="detective-terminal">
      <header className="terminal-header">
        <h1>// AGENCY INTEL CORE: CASE MANAGER</h1>
        <div className="status-badge">SCORE: {score} PTS</div>
      </header>

      {gameState === "START" && (
        <div className="panel central-panel text-center">
          <h2>STOLEN ARTIFACT DOSSIER</h2>
          <p className="subtitle">
            High-value theft flagged. AI tactical reconstruction ready.
          </p>
          <button
            className="btn-action pulse"
            onClick={startNewGame}
            disabled={loading}
          >
            {loading ? "COMPILING SCENARIO..." : "INITIALIZE NEW INVESTIGATION"}
          </button>
        </div>
      )}

      {gameState !== "START" && caseFile && (
        <div className="game-grid">
          {/* Left Column: Crime Scene & Suspects */}
          <div className="column-left">
            <section className="panel incident-report">
              <h3>[CRIME SCENE PROFILE]</h3>
              <p>
                <strong>Target Area:</strong> {caseFile.victim.location}
              </p>
              <p>
                <strong>Asset Lost:</strong> {caseFile.victim.name} (
                {caseFile.victim.value})
              </p>
              <p className="meta-text">
                A security blackout compromised the local array at 9:20 PM.
                Muddy track anomalies and localized physical traces confirmed at
                scene footprint.
              </p>
            </section>

            <section className="panel suspects-roster">
              <h3>[PERSONS OF INTEREST]</h3>
              <div className="suspect-list">
                {caseFile.suspects.map((suspect) => (
                  <div
                    key={suspect.id}
                    className={`suspect-card ${activeSuspectId === suspect.id ? "active" : ""}`}
                    onClick={() => interrogateSuspect(suspect)}
                  >
                    <div>
                      <span className="id-tag">POI-{suspect.id}</span>
                      <strong>{suspect.name}</strong> —{" "}
                      <span className="profession">{suspect.profession}</span>
                    </div>
                    {gameState === "PLAYING" && (
                      <button
                        className="btn-accuse"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleAccuse(suspect.id);
                        }}
                      >
                        ACCUSE
                      </button>
                    )}
                  </div>
                ))}
              </div>
              <div className="warrant-counter">
                Warrants Exercised: {interrogationCount}
              </div>
            </section>
          </div>

          {/* Right Column: Interrogation Monitor & Evidence Log */}
          <div className="column-right">
            <section className="panel monitor-screen">
              <h3>[INTERROGATION FEED]</h3>
              {selectedSuspect ? (
                <div className="feed-content">
                  <h4>TARGET: {selectedSuspect.name.toUpperCase()}</h4>
                  <div className="dialogue-block">
                    <p className="query">
                      Q: State your alibi and location at 9:30 PM.
                    </p>
                    <p className="response">" {selectedSuspect.alibi} "</p>
                  </div>
                  <div className="dialogue-block">
                    <p className="query">
                      Q: What is your connection to the asset?
                    </p>
                    <p className="response">" {selectedSuspect.motive} "</p>
                  </div>
                </div>
              ) : (
                <p className="placeholder-text">
                  Select a POI from the roster to deploy tactical questioning.
                </p>
              )}
            </section>

            <section className="panel evidence-log">
              <div className="panel-header-actions">
                <h3>[EVIDENCE ARTIFACTS]</h3>
                {gameState === "PLAYING" && (
                  <button className="btn-utility" onClick={checkContradictions}>
                    RUN CONTRADICTION CHECK
                  </button>
                )}
              </div>
              <div className="clue-vault">
                {cluesFound.length === 0 ? (
                  <p className="placeholder-text">
                    No hard evidence collected. Initiate interviews to fill
                    database.
                  </p>
                ) : (
                  <ul>
                    {cluesFound.map((clue, index) => (
                      <li
                        key={index}
                        className={
                          clue.startsWith("[PROVEN")
                            ? "alert-clue"
                            : "standard-clue"
                        }
                      >
                        {clue}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </section>
          </div>
        </div>
      )}

      {/* Persistent System Message Ticker */}
      <footer className="system-ticker">
        <span className="ticker-label">SYS_MSG //</span> {systemMessage}
        {(gameState === "WON" || gameState === "LOST") && (
          <button className="btn-reset" onClick={startNewGame}>
            GET the NEW CASE
          </button>
        )}
      </footer>
    </div>
  );
}

export default App;
