import SearchBar from "./SearchBar.tsx";
import Guess from "./Guess.tsx";
import { useState } from "react";

const Game = () => {
    const [guesses, setGuesses] = useState<string[]>([]);

    const addGuess = (guess: string) => {
        setGuesses([...guesses, guess]);
    };

    const answer = "Correct Guess";
    return (
        <div>
            <h1>Guess-A-Game</h1>
            <SearchBar onGuess={addGuess}></SearchBar>
            {guesses
                .map((guess, index) => {
                    return (
                        <Guess
                            key={index}
                            title={guess}
                            answer={answer}
                        ></Guess>
                    );
                })
                .reverse()}
        </div>
    );
};

export default Game;
