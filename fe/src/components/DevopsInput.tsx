import ReusableSkillSelect from "@/components/ReusableSkillSelect";
import { useNavigate } from "react-router";

const DevopsInput = () => {
  const navigate = useNavigate();
  return (
    <ReusableSkillSelect
      title="DevOps/ PM 스택 입력"
      description="본인이 다룰 줄 아는 패키지/빌드/배포 기술 스택을 선택하세요."
      availableSkills={["APT", "Ansible", "Chocolatey", "Composer", "Docker", 
        "Gradle", "Homebrew", "Kubernetes", "MSBuild", "Make", 
        "Maven (build tool)", "NuGet", "Pip", "Podman", "Terraform", 
        "Visual Studio Solution", "Vite", "Webpack", "Yarn", "npm", "pnpm"]}
      onSubmit={(skills) => {
        navigate("/misc-skills");
      }}
    />
  );
};

export default DevopsInput;