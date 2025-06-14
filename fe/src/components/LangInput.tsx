import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";
import { useInputForm } from "@/InputFormStore";


const LangInput = () => {
  const navigate = useNavigate();
const [state, dispatch] = useInputForm();
  return (
    <ReusableSkillSelect
      title="개발 언어 입력"
      description="본인이 다룰 줄 아는 언어를 선택하세요."
      availableSkills={["Bash/Shell (all shells)", "C", "C#", "C++", "Dart", "Go",
        "HTML/CSS", "Java", "JavaScript", "Kotlin", "PHP", "PowerShell",
        "Python", "Ruby", "Rust", "SQL", "TypeScript"]}
      onSubmit={(skills) => {
        dispatch({type: "SET_LANGS", payload:skills});
        navigate("/db-skills");
      }}
    />
  );
};

export default LangInput;