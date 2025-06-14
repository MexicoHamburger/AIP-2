import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TreePine, ArrowDown, Target, Users, Code, Award } from "lucide-react";

interface TreeNode {
  token: string;
  children: string[];
}

interface CareerRoadmapViewProps {
  trees: TreeNode[];
  title?: string;
}

const CareerRoadmapView: React.FC<CareerRoadmapViewProps> = ({ 
  trees, 
  title = "진로 로드맵" 
}) => {
  const getRoleIcon = (token: string) => {
    if (token.toLowerCase().includes('devops')) return <Code className="h-4 w-4" />;
    if (token.toLowerCase().includes('proj')) return <Target className="h-4 w-4" />;
    if (token.toLowerCase().includes('award')) return <Award className="h-4 w-4" />;
    if (token.toLowerCase().includes('club')) return <Users className="h-4 w-4" />;
    return <Code className="h-4 w-4" />;
  };

  const getRoleColor = (token: string) => {
    const colors = {
      'devops': 'bg-blue-500/20 text-blue-300 border-blue-500/30',
      'proj': 'bg-green-500/20 text-green-300 border-green-500/30',
      'award': 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
      'club': 'bg-purple-500/20 text-purple-300 border-purple-500/30',
      'be': 'bg-orange-500/20 text-orange-300 border-orange-500/30',
      'de': 'bg-red-500/20 text-red-300 border-red-500/30',
      'univ': 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
      'outer': 'bg-pink-500/20 text-pink-300 border-pink-500/30'
    };
    
    for (const [key, value] of Object.entries(colors)) {
      if (token.toLowerCase().includes(key)) {
        return value;
      }
    }
    return 'bg-gray-500/20 text-gray-300 border-gray-500/30';
  };

  const formatToken = (token: string) => {
    return token.replace(/["']/g, '').replace(/_/g, ' ').replace(/\|/g, ' | ');
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent mb-2 flex items-center justify-center gap-3">
          <TreePine className="h-8 w-8 text-green-400" />
          {title}
        </h2>
        <p className="text-gray-400">당신의 미래를 위한 {trees.length}가지 성장 경로</p>
      </div>

      <div className="grid gap-8 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1">
        {trees.map((tree, treeIndex) => (
          <div key={treeIndex} className="relative">
            {/* Tree Container */}
            <Card className="bg-gradient-to-br from-gray-900/90 to-gray-800/90 border border-gray-700/50 backdrop-blur-sm hover:border-gray-600/50 transition-all duration-300">
              <CardContent className="p-8">
                {/* Root Node */}
                <div className="text-center mb-8">
                  <div className="relative inline-block">
                    <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-full p-4 mb-4 shadow-lg shadow-green-500/20">
                      <TreePine className="h-8 w-8 text-white" />
                    </div>
                    <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
                      <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-white my-2">
                    경로 #{treeIndex + 1}
                  </h3>
                  
                  <Badge className={`${getRoleColor(tree.token)} mb-4`}>
                    {formatToken(tree.token)}
                  </Badge>
                </div>

                {/* Connecting Line */}
                <div className="flex justify-center mb-6">
                  <div className="w-px h-8 bg-gradient-to-b from-green-500 to-blue-500"></div>
                </div>

                {/* Arrow Down */}
                <div className="flex justify-center mb-6">
                  <ArrowDown className="h-6 w-6 text-blue-400 animate-bounce" />
                </div>

                {/* Branch Nodes */}
                <div className="space-y-6">
                  {tree.children.map((child, childIndex) => (
                    <div key={childIndex} className="relative">
                      {/* Branch Line */}
                      <div className="absolute left-0 top-0 bottom-0 w-px bg-gradient-to-b from-blue-500/50 to-purple-500/50"></div>
                      
                      <div className="pl-6">
                        <div className="bg-gray-800/60 border border-gray-600/40 rounded-lg p-4 hover:bg-gray-800/80 transition-all duration-200 hover:scale-105">
                          <div className="flex items-start gap-3">
                            <div className="flex-shrink-0 mt-1">
                              {getRoleIcon(child)}
                            </div>
                            
                            <div className="flex-1 min-w-0">
                              <Badge className={`${getRoleColor(child)} text-xs`}>
                                {formatToken(child)}
                              </Badge>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Branch Connection Dot */}
                      <div className="absolute left-0 top-6 w-2 h-2 bg-blue-500 rounded-full transform -translate-x-1/2"></div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Tree Shadow Effect */}
            <div className="absolute inset-0 bg-gradient-to-br from-green-600/5 to-blue-600/5 rounded-lg blur-xl -z-10 transform scale-110"></div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CareerRoadmapView;