import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

const EmbeddedInput = () => {
  const navigate = useNavigate();
  return (
    <ReusableSkillSelect
      title="임베디드 스택 입력"
      description="본인이 다룰 줄 아는 임베디드 기술 스택을 선택하세요."
      availableSkills={["Arduino", "CMake", "Cargo", "GNU GCC", "LLVM's Clang", "Rasberry Pi"]}
      onSubmit={() => {
        navigate("/devops-skills");
      }}
    />
  );
};

export default EmbeddedInput;