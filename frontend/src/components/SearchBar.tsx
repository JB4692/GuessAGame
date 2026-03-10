import { useState, useEffect, useRef } from "react";
import Fuse from "fuse.js";

interface SearchBarProps {
    options: string[];
    onGuess: (guess: string) => void;
}

// const SearchBar = ({ options, onGuess }: SearchBarProps) => {
//     const [input, setInput] = useState("");
//     const [results, setResults] = useState<string[]>([]);

//     const fuse = new Fuse(options, {
//         threshold: 0.4, // 0 = exact match, 1 = match anything
//     });

//     const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//         const value = e.target.value;
//         setInput(value);

//         if (value.trim() !== "") {
//             const searchResults = fuse.search(value);
//             setResults(searchResults.map((r) => r.item));
//         } else {
//             setResults([]);
//         }
//     };

//     return (
//         <>
//             <div>
//                 <label>Search:</label>
//                 <input value={input} onChange={handleChange} />
//                 {results.map((result) => (
//                     <div
//                         className="guess"
//                         key={result}
//                         onClick={() => {
//                             onGuess(result);
//                             setInput("");
//                             setResults([]);
//                         }}
//                     >
//                         {result}
//                     </div>
//                 ))}
//                 <button
//                     onClick={() => {
//                         if (input.trim() !== "") {
//                             onGuess(input);
//                             setInput("");
//                         }
//                     }}
//                 >
//                     Check
//                 </button>
//             </div>
//             <div>
//                 <label>Search:</label>
//                 <input
//                     value={input}
//                     onChange={(e) => setInput(e.target.value)}
//                     list="games"
//                 />

//                 <datalist id="games">
//                     {options.map((option) => (
//                         <option key={option} value={option} />
//                     ))}
//                 </datalist>
//                 <button
//                     onClick={() => {
//                         if (input.trim() !== "") {
//                             onGuess(input);
//                             setInput("");
//                         }
//                     }}
//                 >
//                     Check
//                 </button>
//             </div>
//         </>
//     );
// };

const SearchBar = ({ options, onGuess }: SearchBarProps) => {
    const [input, setInput] = useState("");
    const [results, setResults] = useState<string[]>([]);
    const wrapperRef = useRef<HTMLDivElement>(null);

    const fuse = new Fuse(options, { threshold: 0.4 });

    // close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (
                wrapperRef.current &&
                !wrapperRef.current.contains(e.target as Node)
            ) {
                setResults([]);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () =>
            document.removeEventListener("mousedown", handleClickOutside);
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
        onGuess(result);
        setInput("");
        setResults([]);
    };

    return (
        <div ref={wrapperRef} style={{ position: "relative" }}>
            <input
                value={input}
                onChange={handleChange}
                placeholder="Search for a game..."
            />
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
