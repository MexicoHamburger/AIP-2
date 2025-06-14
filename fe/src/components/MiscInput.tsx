import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

import { useInputForm } from "@/InputFormStore";

const MiscInput = () => {
    const navigate = useNavigate();
    const [state, dispatch] = useInputForm();
    return (
        <ReusableSkillSelect
            title="그 외 기술 선택"
            description="아래 목록 중 사용해본 기술들을 선택해주세요."
            availableSkills={[".NET (5+)", ".NET Framework (1.0 - 4.8)", "Apache Kafka", "Flutter",
                "NumPy", "Pandas", "RabbitMQ", "React Native", "Scikit-Learn", "Git",
                "Spring Framework", "TensorFlow", "Torch/PyTorch"]}
            onSubmit={(selected) => {
                dispatch({ type: "SET_TOOLS", payload: selected });
                navigate("/prof")
            }}
        />
    );
};

export default MiscInput;
