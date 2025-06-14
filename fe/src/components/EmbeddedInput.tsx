import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

import { useInputForm } from "@/InputFormStore";

const EmbeddedInput = () => {
  const navigate = useNavigate();
  const [state, dispatch] = useInputForm();
  return (
    <ReusableSkillSelect
      title="임베디드 스택 입력"
      description="본인이 다룰 줄 아는 임베디드 기술 스택을 선택하세요."
      availableSkills={["Arduino", "CMake", "Cargo", "GNU GCC", "LLVM's Clang", "Rasberry Pi"]}
      onSubmit={(skills) => {
        dispatch({ type: "SET_EMB", payload: skills });
        navigate("/devops-skills");
      }}
    />
  );
};

export default EmbeddedInput;