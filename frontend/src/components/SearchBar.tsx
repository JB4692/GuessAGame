import { useState, useEffect, useRef } from "react";
import Fuse from "fuse.js";

interface SearchBarProps {
    options: string[];
    onGuess: (guess: string) => void;
    guessCount: number;
}

const SearchBar = ({ options, onGuess, guessCount }: SearchBarProps) => {
    const [input, setInput] = useState("");
    const [results, setResults] = useState<string[]>([]);
    const wrapperRef = useRef<HTMLDivElement>(null);

    const fuse = new Fuse(options, { threshold: 0.4 });

    // close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
                setResults([]);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setInput(value);
        if (value.trim() !== "") {
            setResults(fuse.search(value).map((r) => r.item));
        } else {
            setResults([]);
        }
    };

    const handleSelect = (result: string) => {
        if (guessCount < 5) {
            onGuess(result);
        }
        setInput("");
        setResults([]);
    };

    return (
        <div ref={wrapperRef}>
            <input value={input} onChange={handleChange} placeholder="Search for a game..." />
            {results.length > 0 && (
                <div
                    style={{
                        maxHeight: "200px",
                        overflowY: "scroll",
                        border: "1px solid #ccc",
                        position: "absolute",
                        background: "white",
                        width: "100%",
                    }}
                >
                    {results.map((result) => (
                        <div
                            key={result}
                            style={{ padding: "8px", cursor: "pointer" }}
                            onClick={() => handleSelect(result)}
                        >
                            {result}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SearchBar;
