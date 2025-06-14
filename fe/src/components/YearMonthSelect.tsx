import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar, ChevronDown } from "lucide-react";

interface YearMonthSelectProps {
  value?: Date;                 // 현재 값 (YYYY-MM-01)
  onChange: (date: Date) => void;
  fromYear?: number;            // 기본 1990
  toYear?: number;              // 기본 올해
}

export default function YearMonthSelect({
  value,
  onChange,
  fromYear = 1990,
  toYear = new Date().getFullYear(),
}: YearMonthSelectProps) {
  // 현재 연·월 파싱 (없으면 기본값: 올해 1월)
  const cur = value ?? new Date(toYear, 0, 1);
  const year = cur.getFullYear();
  const month = cur.getMonth(); // 0-based

  const years = Array.from({ length: toYear - fromYear + 1 }, (_, i) => fromYear + i).reverse(); // 최신년도부터
  const months = Array.from({ length: 12 }, (_, i) => i); // 0~11

  const handleYear = (y: number) => onChange(new Date(y, month, 1));
  const handleMonth = (m: number) => onChange(new Date(year, m, 1));

  const monthNames = [
    "1월", "2월", "3월", "4월", "5월", "6월",
    "7월", "8월", "9월", "10월", "11월", "12월"
  ];

  return (
    <div className="flex items-center gap-3 p-4 bg-gradient-to-r from-gray-900/80 to-gray-800/80 border border-gray-700/50 backdrop-blur-sm rounded-xl">
      <Calendar className="h-5 w-5 text-blue-400 flex-shrink-0" />
      
      <div className="flex gap-2 flex-1">
        {/* 연도 선택 */}
        <div className="flex-1">
          <Select value={String(year)} onValueChange={(v) => handleYear(Number(v))}>
            <SelectTrigger className="w-full bg-gray-800/60 border-gray-600 text-white hover:bg-gray-700/60 hover:border-blue-500/50 transition-all duration-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 h-11 shadow-sm">
              <SelectValue placeholder="연도" />
            </SelectTrigger>
            <SelectContent className="bg-gray-800/95 border-gray-600 text-white backdrop-blur-sm shadow-xl max-h-60 overflow-y-auto">
              {years.map((y) => (
                <SelectItem 
                  key={y} 
                  value={String(y)} 
                  className="focus:bg-blue-600/20 focus:text-blue-200 hover:bg-gray-700/50 cursor-pointer transition-colors duration-150 py-2.5"
                >
                  <span className="font-medium">{y}년</span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* 월 선택 */}
        <div className="flex-1">
          <Select value={String(month)} onValueChange={(v) => handleMonth(Number(v))}>
            <SelectTrigger className="w-full bg-gray-800/60 border-gray-600 text-white hover:bg-gray-700/60 hover:border-blue-500/50 transition-all duration-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 h-11 shadow-sm">
              <SelectValue placeholder="월" />
            </SelectTrigger>
            <SelectContent className="bg-gray-800/95 border-gray-600 text-white backdrop-blur-sm shadow-xl">
              {months.map((m) => (
                <SelectItem 
                  key={m} 
                  value={String(m)} 
                  className="focus:bg-blue-600/20 focus:text-blue-200 hover:bg-gray-700/50 cursor-pointer transition-colors duration-150 py-2.5"
                >
                  <span className="font-medium">{monthNames[m]}</span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* 선택된 날짜 표시 */}
      <div className="text-sm text-gray-400 bg-gray-800/40 px-3 py-2 rounded-lg border border-gray-700/30">
        <span className="text-blue-300 font-medium">
          {year}.{String(month + 1).padStart(2, '0')}
        </span>
      </div>
    </div>
  );
}