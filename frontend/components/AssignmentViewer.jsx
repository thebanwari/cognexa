import React, { useState } from 'react';

const AssignmentViewer = ({ assignments }) => {
  const [expandedQuestions, setExpandedQuestions] = useState(new Set());

  if (!assignments || assignments.length === 0) {
    return null;
  }

  // Group assignments by type
  const groupedAssignments = assignments.reduce((acc, assignment) => {
    const type = assignment.type || 'Unknown';
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push(assignment);
    return acc;
  }, {});

  const toggleQuestion = (index) => {
    const newSet = new Set(expandedQuestions);
    if (newSet.has(index)) {
      newSet.delete(index);
    } else {
      newSet.add(index);
    }
    setExpandedQuestions(newSet);
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'MCQ':
        return '📋';
      case 'SHORT':
        return '📝';
      case 'LONG':
        return '📄';
      default:
        return '❓';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'MCQ':
        return 'from-blue-500 to-blue-600';
      case 'SHORT':
        return 'from-green-500 to-green-600';
      case 'LONG':
        return 'from-purple-500 to-purple-600';
      default:
        return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <div className="space-y-6">
      {Object.entries(groupedAssignments).map(([type, typeAssignments]) => (
        <div key={type} className="space-y-4">
          {/* Type Header */}
          <div className={`bg-gradient-to-r ${getTypeColor(type)} text-white p-4 rounded-lg`}>
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{getTypeIcon(type)}</span>
              <div>
                <h4 className="font-semibold text-lg">{type} Questions</h4>
                <p className="text-sm opacity-90">{typeAssignments.length} question(s)</p>
              </div>
            </div>
          </div>

          {/* Questions */}
          <div className="space-y-4">
            {typeAssignments.map((assignment, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
              >
                {/* Question Header */}
                <button
                  onClick={() => toggleQuestion(`${type}-${index}`)}
                  className="w-full text-left p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="text-sm font-medium text-gray-500">Q{index + 1}</span>
                      <span className="font-medium text-gray-900">{assignment.question}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      {expandedQuestions.has(`${type}-${index}`) ? (
                        <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                        </svg>
                      ) : (
                        <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      )}
                    </div>
                  </div>
                </button>

                {/* Answer Content */}
                {expandedQuestions.has(`${type}-${index}`) && (
                  <div className="p-4 bg-white border-t border-gray-200">
                    <div className="flex items-start space-x-3">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                      <div className="text-gray-700 leading-relaxed">
                        <p className="font-medium text-gray-900 mb-2">Answer:</p>
                        <p>{assignment.answer}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AssignmentViewer;