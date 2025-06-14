// CareerFormStore.tsx
import React, { createContext, useContext, useReducer } from "react";


interface State {
    careerTokens: string[];
    sequenceTokens: string[];
    certTokens: string[];
    langTokens: string[];
    dbTokens: string[];
    platformTokens: string[];
    webTokens: string[];
    embTokens: string[];
    miscTokens: string[];
    toolsTokens: string[];
    profTokens: string[];
    api1Result?: unknown;   // 새로 추가
    api2Result?: unknown;   // 새로 추가
}

type Action =
    | { type: "SET_CAREER"; payload: string[] }
    | { type: "SET_CERTS"; payload: string[] }
    | { type: "SET_LANGS"; payload: string[] }
    | { type: "SET_DB"; payload: string[] }
    | { type: "SET_PLAT"; payload: string[] }
    | { type: "SET_WEB"; payload: string[] }
    | { type: "SET_EMB"; payload: string[] }
    | { type: "SET_MISC"; payload: string[] }
    | { type: "SET_TOOLS"; payload: string[] }
    | { type: "SET_PROF"; payload: string[] }
    | { type: "SET_SEQUENCE"; payload: string[] }
    | { type: "SET_API1_RESULT"; payload: unknown }
    | { type: "SET_API2_RESULT"; payload: unknown }
    | { type: "RESET" };

const initialState: State = {
    careerTokens: [],
    sequenceTokens: [],
    certTokens: [],
    langTokens: [],
    dbTokens: [],
    platformTokens: [],
    webTokens: [],
    embTokens: [],
    miscTokens: [],
    toolsTokens: [],
    profTokens: []
};


/* --------- 리듀서 --------- */
function reducer(state: State, action: Action): State {
    switch (action.type) {
        case "SET_SEQUENCE":
            return { ...state, sequenceTokens: action.payload };
        case "SET_CAREER":
            return { ...state, careerTokens: action.payload };
        case "SET_CERTS":
            return { ...state, certTokens: action.payload };
        case "SET_LANGS":
            return { ...state, langTokens: action.payload };
        case "SET_DB":
            return { ...state, dbTokens: action.payload };
        case "SET_PLAT":
            return { ...state, platformTokens: action.payload };
        case "SET_WEB":
            return { ...state, webTokens: action.payload };
        case "SET_EMB":
            return { ...state, embTokens: action.payload };
        case "SET_MISC":
            return { ...state, miscTokens: action.payload };
        case "SET_TOOLS":
            return { ...state, toolsTokens: action.payload };
        case "SET_PROF":
            return { ...state, profTokens: action.payload };
        case "SET_API1_RESULT":
            return { ...state, api1Result: action.payload };
        case "SET_API2_RESULT":
            return { ...state, api2Result: action.payload };
        case "RESET":
            return initialState;
        default:
            return state;
    }
}

const FormContext = createContext<
    [State, React.Dispatch<Action>] | undefined
>(undefined);

export const InputFormProvider = ({
    children,
}: {
    children: React.ReactNode;
}) => {
    const [state, dispatch] = useReducer(reducer, initialState);
    return (
        <FormContext.Provider value={[state, dispatch]}>
            {children}
        </FormContext.Provider>
    );
};

/* ---------- 커스텀 훅 ---------- */
export const useInputForm = () => {
    const ctx = useContext(FormContext);
    if (!ctx)
        throw new Error("useCareerForm must be used within InputFormProvider");
    return ctx; // [state, dispatch]
};