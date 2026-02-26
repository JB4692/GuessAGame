import { useState } from "react";

interface Props {
    onGuess: (guess: string) => void;
}

const SearchBar = ({ onGuess }: Props) => {
    const [input, setInput] = useState("");
    return (
        <div>
            <label id="game-search" htmlFor="game-search">
                Search:
            </label>
            <input
                id="game-search"
                onChange={(e) => {
                    if (e.target.value.trim() !== "") {
                        setInput(e.target.value);
                    }
                }}
            ></input>
            <button
                onClick={() => {
                    if (input.trim() !== "") {
                        onGuess(input);
                        setInput("");
                    }
                }}
            >
                Check
            </button>
        </div>
    );
};

export default SearchBar;
