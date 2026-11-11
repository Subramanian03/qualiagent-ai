import { useEffect, useState } from "react";

import "./App.css";

import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import AutomationViewerModal from "./components/modals/AutomationViewerModal";
import ExecutionDetailsModal from "./components/modals/ExecutionDetailsModal";
import TestCaseDetailSection from "./components/testcases/TestCaseDetailSection";


import DashboardPage from "./pages/DashboardPage";
import ProjectsPage from "./pages/ProjectsPage";
import ProjectWorkspacePage from "./pages/ProjectWorkspacePage";
import TestCasesPage from "./pages/TestCasesPage";
import AutomationPage from "./pages/AutomationPage";
import ExecutionsPage from "./pages/ExecutionsPage";
import TestCyclesPage from "./pages/TestCyclesPage";
import CycleWorkspacePage from "./pages/CycleWorkspacePage";
import ReportsPage from "./pages/ReportsPage";
import ScenariosPage from "./pages/ScenariosPage";

import {
  getProjectCycleReadiness,
  getProjectTestCycles,
  createTestCycle,
  getTestCycle,
  getTestCycleSummary,
  updateTestCycleStatus,
  updateManualCycleResult,
  getCycleAutomationInputs,
  runCycleAutomation,
  analyseRequirement,
  createExecution,
  createProject,
  createRequirement, 
  getExecution,
  getExecutionScreenshot,
  getExecutionTrace,
  getProjectExecutions,
  getProjects,
  getProjectRequirements,
  getRequirementTestCases,
  generateScenarioTestCases,
  getTestCaseAutomation,
  getReadyTestCaseAutomation,
  getAutomationHistory,
  runExecution,
  updateTestCaseStatus,
  updateTestCaseExecutionType,
  getProjectQualitySummary,
  getProjectCycleQualitySummary,
  getProjectCycleTraceability,
  getRequirementCoverage,
  getRequirementTestScenarios,
  getScenarioTestCases,
  generateRequirementScenarios,
  getAutomationInputSchema,
  generateRealAutomation,
  reviewAutomation,
  getExecutionInputSchema,
  createHumanEditedAutomation,
  createAIUpdatedAutomation,
  getProjectReleaseQuality,
  analyzeExecutionFailure,
  downloadProjectReleaseQualityPdf,
  downloadProjectReleaseQualityExcel,
} from "./services/api";

function App() {
  const [projects, setProjects] = useState([]);
  const [requirements, setRequirements] = useState([]);
  const [testCases, setTestCases] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [currentPage, setCurrentPage] = useState("dashboard");

  const [
  testCycles,
  setTestCycles
] = useState([]);


  const [
  testCyclesLoading,
  setTestCyclesLoading
] = useState(false);


  const [
  cycleReadiness,
  setCycleReadiness
] = useState(null);


  const [
  cycleReadinessLoading,
  setCycleReadinessLoading
] = useState(false);


  const [
  showCycleBuilder,
  setShowCycleBuilder
] = useState(false);


  const [
  creatingTestCycle,
  setCreatingTestCycle
] = useState(false);


  const [
  selectedCycle,
  setSelectedCycle
] = useState(null);

  const [
  cycleSummary,
  setCycleSummary
] = useState(null);


const [
  cycleActionLoading,
  setCycleActionLoading
] = useState(false);


const [
  selectedManualCycleItem,
  setSelectedManualCycleItem
] = useState(null);


const [
  showManualResultModal,
  setShowManualResultModal
] = useState(false);


const [
  manualResultSaving,
  setManualResultSaving
] = useState(false);


const [
  manualResultForm,
  setManualResultForm
] = useState({
    status: "passed",
    actual_result: "",
    comment: "",
    defect_reference: ""
  });


const [
  selectedAutomationCycleItem,
  setSelectedAutomationCycleItem
] = useState(null);


const [
  cycleAutomationSchema,
  setCycleAutomationSchema
] = useState(null);


const [
  cycleAutomationValues,
  setCycleAutomationValues
] = useState({});


const [
  showCycleAutomationModal,
  setShowCycleAutomationModal
] = useState(false);


const [
  preparingCycleAutomationItemId,
  setPreparingCycleAutomationItemId
] = useState(null);


const [
  runningCycleAutomationItemId,
  setRunningCycleAutomationItemId
] = useState(null);


const [
  selectedCycleLoading,
  setSelectedCycleLoading
] = useState(false);

const [
  cycleForm,
  setCycleForm
] = useState({
  name: "",
  release: "",
  environment: "",
  items: {}
});

  const [showProjectForm, setShowProjectForm] = useState(false);

  const [projectForm,setProjectForm] = useState({
          name: "",
          description: "",
          application_type: "web",
          automation_engine: "playwright",
          automation_language: "javascript",
          default_browser: "chromium",
        });

  const [savingProject, setSavingProject] = useState(false);

  const [selectedProject, setSelectedProject] = useState(null);

  const [workspaceRequirements, setWorkspaceRequirements] = useState([]);

  const [workspaceTestCases, setWorkspaceTestCases] = useState([]);

  const [workspaceScenarios,setWorkspaceScenarios] = useState([]);

  const [scenarioTestCases,setScenarioTestCases] = useState({});

  const [scenariosLoading,setScenariosLoading] = useState(false);

  const [workspaceLoading, setWorkspaceLoading] = useState(false);

  const [showRequirementForm, setShowRequirementForm] = useState(false);

  const [savingRequirement, setSavingRequirement] = useState(false);

  const [requirementForm, setRequirementForm] = useState({
    requirement_id: "",
    title: "",
    description: "",
    application_type: "web",
  });

  const [selectedRequirement, setSelectedRequirement] = useState(null);

  const [requirementAnalysis, setRequirementAnalysis] = useState(null);

  const [
  projectReleaseQuality,
  setProjectReleaseQuality
] = useState(null);

  const [
  releasePdfDownloading,
  setReleasePdfDownloading
] = useState(false);

  const [
  releaseExcelDownloading,
  setReleaseExcelDownloading
] = useState(false);

  const [analysingRequirementId, setAnalysingRequirementId] = useState(null);

  const [showAnalysisModal, setShowAnalysisModal] = useState(false);

  const [generatingScenariosRequirementId,setGeneratingScenariosRequirementId] = useState(null);

  const [generatingScenarioTestCasesId,setGeneratingScenarioTestCasesId] = useState(null);

  const [selectedTestCase, setSelectedTestCase] = useState(null);

  const [showTestCaseModal, setShowTestCaseModal] = useState(false);

  const [updatingTestCaseId, setUpdatingTestCaseId] = useState(null);

  const [updatingExecutionTypeId,setUpdatingExecutionTypeId] = useState(null);

  const [selectedAutomation, setSelectedAutomation] = useState(null);

  const [selectedAutomationTestCase, setSelectedAutomationTestCase] = useState(null);

  const [loadingAutomationId, setLoadingAutomationId] = useState(null);

  const [showAutomationModal, setShowAutomationModal] = useState(false);

  const [automationHistory,setAutomationHistory] = useState([]);

  const [automationHistoryLoading,setAutomationHistoryLoading] = useState(false);

  const [reviewingAutomationId,setReviewingAutomationId] = useState(null);

  const [savingAutomationEditId, setSavingAutomationEditId] = useState(null);

  const [updatingAutomationWithAIId, setUpdatingAutomationWithAIId] = useState(null);

  const [generatingRealAutomationId,setGeneratingRealAutomationId] = useState(null);

  const [automationByTestCase, setAutomationByTestCase] = useState({});

  const [automationInputSchema,setAutomationInputSchema] = useState(null);

  const [automationInputValues,setAutomationInputValues] = useState({});

  const [preparingAutomationTestCase,setPreparingAutomationTestCase] = useState(null);

  const [preparingAutomationId,setPreparingAutomationId] = useState(null);

  const [showAutomationInputModal,setShowAutomationInputModal] = useState(false);

  const [selectedExecution,setSelectedExecution] = useState(null);

  const [executionTestCase,setExecutionTestCase] = useState(null);
  
  const [executionAutomation,setExecutionAutomation] = useState(null);
  
  const [runningTestCaseId,setRunningTestCaseId] = useState(null);

  const [showRunModal,setShowRunModal] = useState(false);

  const [executionInputSchema,setExecutionInputSchema] = useState(null);

  const [executionInputValues,setExecutionInputValues] = useState({});

  const [preparingExecutionInputs,setPreparingExecutionInputs] = useState(false);

  const [projectExecutions,setProjectExecutions] = useState([]);

  const [executionsLoading,setExecutionsLoading] = useState(false);

  const [selectedHistoryExecution,setSelectedHistoryExecution] = useState(null);

  const [
  failureAnalysis,
  setFailureAnalysis
] = useState(null);


const [
  failureAnalysisLoading,
  setFailureAnalysisLoading
] = useState(false);


const [
  failureAnalysisError,
  setFailureAnalysisError
] = useState("");

  const [projectQualitySummary,setProjectQualitySummary] = useState(null);

  const [projectCycleQualitySummary,setProjectCycleQualitySummary] = useState(null);

  const [ projectCycleTraceability,setProjectCycleTraceability] = useState(null);

  const [
  reportFilters,
  setReportFilters
] = useState({
  release: "",
  environment: "",
  cycle_status: "",
  result_status: "",
  execution_mode: ""
});

  const [reportFiltersLoading,setReportFiltersLoading] = useState(false);

  const [reportsLoading,setReportsLoading] = useState(false);

  const [dashboardQualitySummary,setDashboardQualitySummary] = useState(null);

  const [requirementCoverage,setRequirementCoverage] = useState([]);

  const [showExecutionDetailsModal,setShowExecutionDetailsModal] = useState(false);

  const [historyScreenshotUrl,setHistoryScreenshotUrl] = useState(null);

  const [historyScreenshotLoading,setHistoryScreenshotLoading] = useState(false);
  
  const [screenshotUrl,setScreenshotUrl] = useState(null);

  const [screenshotLoading,setScreenshotLoading] = useState(false);
  
  function resetCycleForm() {
  setCycleForm({
    name: "",
    release: "",
    environment: "",
    items: {}
  });
}

  function handleCycleFormChange(
  event
) {
  const {
    name,
    value
  } = event.target;


  setCycleForm(
    (current) => ({
      ...current,
      [name]: value
    })
  );
}

  function handleCycleTestCaseSelection(
  testCase,
  selected
) {
  setCycleForm(
    (current) => {

      const items = {
        ...current.items
      };


      if (!selected) {

        delete items[
          testCase.id
        ];


        return {
          ...current,
          items
        };
      }


      let executionMode =
        "manual";


      if (
        !testCase.manual_eligible &&
        testCase.automation_eligible
      ) {
        executionMode =
          "automation";
      }


      items[testCase.id] = {
        selected: true,
        execution_mode:
          executionMode
      };


      return {
        ...current,
        items
      };
    }
  );
}

  function handleCycleExecutionMode(
  testCase,
  executionMode
) {
  if (
    executionMode === "manual" &&
    !testCase.manual_eligible
  ) {
    return;
  }


  if (
    executionMode ===
      "automation" &&
    !testCase.automation_eligible
  ) {
    return;
  }


  setCycleForm(
    (current) => ({
      ...current,

      items: {
        ...current.items,

        [testCase.id]: {
          selected: true,

          execution_mode:
            executionMode
        }
      }
    })
  );
}

  function getSelectedCycleItemCount() {
  return Object.keys(
    cycleForm.items || {}
  ).length;
}

  async function handleCreateTestCycle(
  event
) {
  event.preventDefault();


  if (!selectedProject) {
    return;
  }


  const items = Object.entries(
    cycleForm.items || {}
  ).map(
    ([
      testCaseId,
      value
    ]) => ({
      test_case_id:
        Number(testCaseId),

      execution_mode:
        value.execution_mode
    })
  );


  if (items.length === 0) {

    setError(
      "Select at least one Test Case "
      + "for the Test Cycle."
    );

    return;
  }


  try {

    setCreatingTestCycle(
      true
    );


    setError("");


    const createdCycle =
      await createTestCycle(
        selectedProject.id,
        {
          name:
            cycleForm.name
              .trim(),

          release:
            cycleForm.release
              .trim() || null,

          environment:
            cycleForm.environment
              .trim() || null,

          items
        }
      );


    setShowCycleBuilder(
      false
    );


    resetCycleForm();


    setSelectedCycle(
      createdCycle
    );


    await loadProjectTestCycles(
      selectedProject.id
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to create Test Cycle."
    );


  } finally {

    setCreatingTestCycle(
      false
    );
  }
}

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const projectData = await getProjects();

      setProjects(projectData);

      if (projectData.length === 0) {
        setRequirements([]);
        setTestCases([]);

        setSelectedProject(null);
        setWorkspaceRequirements([]);
        setWorkspaceTestCases([]);
        setWorkspaceScenarios([]);
        setScenarioTestCases({});
        setProjectQualitySummary(
  null
);

setProjectCycleQualitySummary(
  null
);

setProjectCycleTraceability(
  null
);

setRequirementCoverage(
  []
);

setProjectReleaseQuality(
  null
);
        setDashboardQualitySummary(null);

        return;
      }

      const currentProject = projectData[0];

      const requirementData = await getProjectRequirements(currentProject.id);

      const testCaseGroups = await Promise.all(
        requirementData.map((requirement) =>
          getRequirementTestCases(requirement.id),
        ),
      );

      const loadedTestCases = testCaseGroups.flat();

      const qualitySummary =
         await getProjectQualitySummary(
          currentProject.id
        );

       setDashboardQualitySummary(qualitySummary);

      /*
       * Dashboard state
       */
      setRequirements(requirementData);

      setTestCases(loadedTestCases);

      /*
       * Default selected project
       */
      setSelectedProject(currentProject);

      /*
       * Initialise workspace state
       * using the exact same project data.
       */
      setWorkspaceRequirements(requirementData);

      setWorkspaceTestCases(loadedTestCases);
      await loadScenarioWorkspace(requirementData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadScenarioWorkspace(
  requirementData
) {
  try {
    setScenariosLoading(true);

    if (
      !Array.isArray(
        requirementData
      ) ||
      requirementData.length === 0
    ) {
      setWorkspaceScenarios([]);
      setScenarioTestCases({});

      return;
    }


    const scenarioGroups =
      await Promise.all(
        requirementData.map(
          (requirement) =>
            getRequirementTestScenarios(
              requirement.id
            )
        )
      );


    const scenarios =
      scenarioGroups.flat();


    setWorkspaceScenarios(
      scenarios
    );


    if (scenarios.length === 0) {
      setScenarioTestCases({});

      return;
    }


    const testCaseEntries =
      await Promise.all(
        scenarios.map(
          async (scenario) => {

            const cases =
              await getScenarioTestCases(
                scenario.id
              );

            return [
              scenario.id,
              Array.isArray(cases)
                ? cases
                : []
            ];
          }
        )
      );


    setScenarioTestCases(
      Object.fromEntries(
        testCaseEntries
      )
    );


  } catch (err) {

    console.error(
      "Scenario workspace load failed:",
      err
    );

    setError(
      err.message ||
      "Failed to load Scenario workspace."
    );

  } finally {
    setScenariosLoading(false);
  }
}

  async function loadProjectWorkspace(project) {
    try {
      setWorkspaceLoading(true);
      setError("");

      const requirementData = await getProjectRequirements(project.id);

      setWorkspaceRequirements(requirementData);

      await loadScenarioWorkspace(
  requirementData
);

      const testCaseGroups = await Promise.all(
        requirementData.map((requirement) =>
          getRequirementTestCases(requirement.id),
        ),
      );

      setWorkspaceTestCases(testCaseGroups.flat());
    } catch (err) {
      setError(err.message);
    } finally {
      setWorkspaceLoading(false);
    }
  }



  async function openProject(
  project
) {
  setSelectedProject(
    project
  );


  /*
   * Clear data belonging to the
   * previously selected Project.
   */
  setWorkspaceRequirements([]);

  setWorkspaceTestCases([]);

  setWorkspaceScenarios([]);

  setScenarioTestCases({});

  setProjectQualitySummary(
  null
);

setProjectCycleQualitySummary(
  null
);

setProjectCycleTraceability(
  null
);

setProjectReleaseQuality(
  null
);

setRequirementCoverage(
  []
);

setProjectExecutions(
  []
);

setReportFilters({
  release: "",
  environment: "",
  cycle_status: "",
  result_status: "",
  execution_mode: ""
});


  /*
   * Clear Test Cycle state so Cycle
   * data cannot leak between Projects.
   */
  setTestCycles([]);

  setCycleReadiness(null);

  setSelectedCycle(null);

  setShowCycleBuilder(false);

  resetCycleForm();

  setCycleSummary(
  null
);


setShowManualResultModal(
  false
);

setSelectedManualCycleItem(
  null
);

resetManualResultForm();


setShowCycleAutomationModal(
  false
);

setSelectedAutomationCycleItem(
  null
);

setCycleAutomationSchema(
  null
);

setCycleAutomationValues(
  {}
);

setPreparingCycleAutomationItemId(
  null
);

setRunningCycleAutomationItemId(
  null
);



  setCurrentPage(
    "workspace"
  );


  await loadProjectWorkspace(
    project
  );
}

  async function openRequirementsPage() {
  const project =
    selectedProject ||
    projects[0];

  if (!project) {
    setError(
      "No project is available for Requirements."
    );

    return;
  }

  try {
    setError("");

    setSelectedProject(
      project
    );

    await loadProjectWorkspace(
      project
    );

    setCurrentPage(
      "requirements"
    );

  } catch (err) {
    setError(err.message);
  }
}

  async function openTestCasesPage() {
    const project = selectedProject || projects[0];

    if (!project) {
      setError("No project is available for Test Cases.");

      return;
    }

    try {
      setError("");
      setWorkspaceLoading(true);

      setSelectedProject(project);

      const requirementData = await getProjectRequirements(project.id);

      const testCaseGroups = await Promise.all(
        requirementData.map((requirement) =>
          getRequirementTestCases(requirement.id),
        ),
      );

      setWorkspaceRequirements(requirementData);

      setWorkspaceTestCases(testCaseGroups.flat());

      setCurrentPage("test-cases");
    } catch (err) {
      setError(err.message);
    } finally {
      setWorkspaceLoading(false);
    }
  }

  function handleProjectChange(
  event
) {
  const {
    name,
    value
  } = event.target;


  setProjectForm(
    (current) => {

      /*
       * Changing automation engine also
       * changes the currently supported
       * language automatically.
       */
      if (
        name ===
        "automation_engine"
      ) {

        return {
          ...current,

          automation_engine:
            value,

          automation_language:
            value === "selenium"
              ? "python"
              : "javascript",
        };
      }


      return {
  ...current,
  [name]: value,
};
    }
  );
}

  async function handleCreateProject(event) {
    event.preventDefault();

    try {
      setSavingProject(true);
      setError("");

      await createProject(projectForm);

      setProjectForm({
  name: "",
  description: "",
  application_type: "web",
  automation_engine: "playwright",
  automation_language: "javascript",
  default_browser: "chromium",
});

      setShowProjectForm(false);

      await loadDashboard();

      setCurrentPage("projects");
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingProject(false);
    }
  }

  function handleRequirementChange(event) {
    const { name, value } = event.target;

    setRequirementForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleCreateRequirement(event) {
    event.preventDefault();

    if (!selectedProject) {
      return;
    }

    try {
      setSavingRequirement(true);
      setError("");

      await createRequirement(selectedProject.id, requirementForm);

      setShowRequirementForm(false);

      setRequirementForm({
        requirement_id: "",
        title: "",
        description: "",
        application_type: selectedProject.application_type,
      });

      await loadProjectWorkspace(selectedProject);

      await loadDashboard();
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingRequirement(false);
    }
  }

  async function handleAnalyseRequirement(requirement) {
    try {
      setAnalysingRequirementId(requirement.id);

      setError("");

      setSelectedRequirement(requirement);

      const analysis = await analyseRequirement(requirement);

      setRequirementAnalysis(analysis);

      setShowAnalysisModal(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setAnalysingRequirementId(null);
    }
  }

  async function handleGenerateScenarios(
  requirement
) {
  if (!selectedProject) {
    return;
  }

  try {
    setGeneratingScenariosRequirementId(
      requirement.id
    );

    setError("");

    setSelectedRequirement(
      requirement
    );

    await generateRequirementScenarios(
      requirement.id
    );

    await loadProjectWorkspace(
      selectedProject
    );

    setCurrentPage(
      "scenarios"
    );

  } catch (err) {
    setError(err.message);
  } finally {
    setGeneratingScenariosRequirementId(
      null
    );
  }
}

  async function handleGenerateScenarioTestCases(
  scenario
) {
  if (
    !selectedProject ||
    !selectedRequirement
  ) {
    setError(
      "Project or Requirement context is missing."
    );

    return;
  }

  try {
    setGeneratingScenarioTestCasesId(
      scenario.id
    );

    setError("");

    await generateScenarioTestCases(
      scenario.id
    );

    const requirementData =
      await getProjectRequirements(
        selectedProject.id
      );

    setWorkspaceRequirements(
      requirementData
    );

    await loadScenarioWorkspace(
      requirementData
    );

    const testCaseGroups =
      await Promise.all(
        requirementData.map(
          (requirement) =>
            getRequirementTestCases(
              requirement.id
            )
        )
      );

    setWorkspaceTestCases(
      testCaseGroups.flat()
    );

    setCurrentPage(
      "scenarios"
    );

  } catch (err) {
    setError(
      err.message
    );

  } finally {
    setGeneratingScenarioTestCasesId(
      null
    );
  }
}


  function getRequirementTestCount(requirementId) {
    return workspaceTestCases.filter(
      (testCase) => testCase.requirement_db_id === requirementId,
    ).length;
  }

  function getRequirementScenarioCount(
  requirementId
) {
  return workspaceScenarios.filter(
    (scenario) =>
      scenario.requirement_db_id ===
      requirementId
  ).length;
}

  function getRequirementAIScenarioCount(
  requirementId
) {
  return workspaceScenarios.filter(
    (scenario) =>
      scenario.requirement_db_id ===
        requirementId &&
      scenario.source === "ai"
  ).length;
}

  function handleViewScenarios(
  requirement
) {
  setSelectedRequirement(
    requirement
  );

  setCurrentPage(
    "scenarios"
  );
}

  function openTestCase(testCase) {
    setSelectedTestCase(testCase);

    setShowTestCaseModal(true);
  }

  function getRequirementTitle(requirementDbId) {
    const requirement = workspaceRequirements.find(
      (item) => item.id === requirementDbId,
    );

    return requirement ? requirement.title : "Unknown requirement";
  }

  async function handleTestCaseStatus(
  testCase,
  reviewStatus
) {
  if (!selectedProject) {
    return;
  }

  const pageBeforeUpdate =
    currentPage;

  const requirementBeforeUpdate =
    selectedRequirement;

  try {
    setUpdatingTestCaseId(
      testCase.id
    );

    setError("");

    const updatedTestCase =
      await updateTestCaseStatus(
        testCase.id,
        reviewStatus
      );


    /*
     * Keep the Test Case Details modal
     * showing the newly updated record.
     */
    setSelectedTestCase(
      updatedTestCase
    );


    /*
     * Refresh only data belonging to the
     * currently selected project.
     *
     * Do NOT call loadDashboard() here.
     */
    await loadProjectWorkspace(
      selectedProject
    );


    /*
     * Reports use approval counts, so
     * refresh the quality summary without
     * navigating away.
     */
    await loadProjectQualitySummary(
      selectedProject
    );


    /*
     * Preserve the page from which the
     * tester approved/rejected the case.
     */
    setSelectedRequirement(
      requirementBeforeUpdate
    );

    setCurrentPage(
      pageBeforeUpdate
    );


  } catch (err) {

    setError(
      err.message
    );

  } finally {

    setUpdatingTestCaseId(
      null
    );
  }
}

  async function handleTestCaseExecutionType(
  testCase,
  executionType
) {
  if (!selectedProject) {
    return;
  }


  try {

    setUpdatingExecutionTypeId(
      testCase.id
    );

    setError("");


    const updatedTestCase =
      await updateTestCaseExecutionType(
        testCase.id,
        executionType
      );


    /*
     * Keep the open details modal
     * synchronized.
     */
    setSelectedTestCase(
      updatedTestCase
    );


    /*
     * Update workspace Test Case state
     * immediately.
     */
    setWorkspaceTestCases(
      (current) =>
        current.map(
          (item) =>
            item.id ===
            updatedTestCase.id
              ? updatedTestCase
              : item
        )
    );


    /*
     * Scenario page has its own
     * scenario -> Test Cases map.
     */
    setScenarioTestCases(
      (current) => {

        const updated = {
          ...current
        };


        for (
          const scenarioId
          of Object.keys(updated)
        ) {

          updated[scenarioId] =
            (
              updated[scenarioId] ||
              []
            ).map(
              (item) =>
                item.id ===
                updatedTestCase.id
                  ? updatedTestCase
                  : item
            );
        }


        return updated;
      }
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to update execution type."
    );


  } finally {

    setUpdatingExecutionTypeId(
      null
    );
  }
}

  function getReviewStatus(testCase) {
    return testCase?.review_status || "draft";
  }

  async function handlePrepareAutomation(
  testCase
) {
  try {
    setPreparingAutomationId(
      testCase.id
    );

    setError("");

    setPreparingAutomationTestCase(
      testCase
    );

    const schema =
      await getAutomationInputSchema(
    testCase.id
  );
  

    const initialValues = {};

    for (
      const input of schema.inputs || []
    ) {
      initialValues[input.key] =
        input.input_type === "boolean"
          ? false
          : "";
    }

    setAutomationInputSchema(
      schema
    );

    setAutomationInputValues(
      initialValues
    );

    setShowAutomationInputModal(
      true
    );

  } catch (err) {
    setAutomationInputSchema(null);
    setAutomationInputValues({});
    setPreparingAutomationTestCase(null);

    setError(err.message);

  } finally {
    setPreparingAutomationId(null);
  }
}

  function handleAutomationInputChange(
  input,
  event
) {
  const value =
    input.input_type === "boolean"
      ? event.target.checked
      : event.target.value;

  setAutomationInputValues(
    (current) => ({
      ...current,
      [input.key]: value
    })
  );
}

  function closeAutomationInputModal() {
  setShowAutomationInputModal(false);

  setAutomationInputSchema(null);
  setAutomationInputValues({});
  setPreparingAutomationTestCase(null);
}

  async function handleAutomationInputContinue(
  event
) {
  event.preventDefault();

  if (
    !automationInputSchema ||
    !preparingAutomationTestCase
  ) {
    return;
  }


  const testCase =
    preparingAutomationTestCase;

  /*
   * Take a temporary snapshot.
   * Do not log this object because it
   * can contain credentials.
   */
  const submittedValues = {
    ...automationInputValues
  };


  try {
    setGeneratingRealAutomationId(
      testCase.id
    );

    setError("");


    const automation =
      await generateRealAutomation(
        testCase.id,
        submittedValues
      );


    /*
     * Clear runtime values immediately
     * after the request completes.
     */
    setAutomationInputValues({});


    /*
     * Keep Automation Workspace state
     * synchronised with the newly-created
     * DRAFT automation.
     */
    setAutomationByTestCase(
      (current) => ({
        ...current,
        [testCase.id]: automation
      })
    );


    /*
     * Close the runtime-data popup.
     */
    setShowAutomationInputModal(
      false
    );

    setAutomationInputSchema(
      null
    );


    /*
     * Configure existing Automation Viewer.
     */
    setSelectedAutomationTestCase(
      testCase
    );

    setSelectedAutomation(
      automation
    );

    setPreparingAutomationTestCase(
      null
    );


    /*
     * Open generated DRAFT source
     * for human review.
     */
    setShowAutomationModal(
      true
    );


  } catch (err) {

    /*
     * Clear runtime values even when
     * generation fails.
     *
     * Passwords/tokens must not remain in
     * React state after the request.
     */
    setAutomationInputValues({});

    setError(
      err.message ||
      "Real automation generation failed."
    );


  } finally {

    /*
     * Also clear our local snapshot.
     */
    for (
      const key of
      Object.keys(submittedValues)
    ) {
      submittedValues[key] = "";
    }


    setGeneratingRealAutomationId(
      null
    );
  }
}

  async function handleOpenRunTest(
  testCase
) {
  /*
   * Open the modal immediately.
   * Do not wait for AI input analysis.
   */
  setExecutionTestCase(
    testCase
  );

  setExecutionAutomation(
    null
  );

  setExecutionInputSchema(
    null
  );

  setExecutionInputValues(
    {}
  );

  setSelectedExecution(
    null
  );

  setShowRunModal(
    true
  );


  if (screenshotUrl) {
    URL.revokeObjectURL(
      screenshotUrl
    );

    setScreenshotUrl(
      null
    );
  }


  try {

    setPreparingExecutionInputs(
      true
    );

    setError("");


    const automation =
  await getReadyTestCaseAutomation(
    testCase.id
  );


    if (
      !automation ||
      automation.status !== "ready"
    ) {

      throw new Error(
        "READY automation is required "
        + "before execution."
      );
    }


    setExecutionAutomation(
      automation
    );


    const schema =
      await getExecutionInputSchema(
    testCase.id
  );


    const initialValues = {};


    for (
      const input of
      schema.inputs || []
    ) {

      initialValues[
        input.key
      ] =
        input.input_type ===
        "boolean"
          ? false
          : "";
    }


    setExecutionInputSchema(
      schema
    );

    setExecutionInputValues(
      initialValues
    );


  } catch (err) {

    setExecutionAutomation(
      null
    );

    setExecutionInputSchema(
      null
    );

    setExecutionInputValues(
      {}
    );

    setError(
      err.message ||
      "Unable to prepare execution."
    );


  } finally {

    setPreparingExecutionInputs(
      false
    );
  }
}
  
  function handleExecutionInputChange(
  input,
  event
) {
  const value =
    input.input_type === "boolean"
      ? event.target.checked
      : event.target.value;


  setExecutionInputValues(
    (current) => ({
      ...current,
      [input.key]: value
    })
  );
}

  function closeRunModal() {
  if (runningTestCaseId !== null) {
    return;
  }

  setExecutionInputValues({});
  setExecutionInputSchema(null);

  setShowRunModal(false);

  setSelectedExecution(null);
  setExecutionTestCase(null);
  setExecutionAutomation(null);

  setPreparingExecutionInputs(false);

  if (screenshotUrl) {
    URL.revokeObjectURL(
      screenshotUrl
    );
  }

  setScreenshotUrl(null);
}

  async function handleRunTest() {

  if (
    !executionTestCase ||
    !executionAutomation ||
    !executionInputSchema
  ) {
    return;
  }


  const submittedValues = {
    ...executionInputValues
  };


  try {

    setRunningTestCaseId(
      executionTestCase.id
    );

    setError("");

    setSelectedExecution(
      null
    );


    const execution =
      await createExecution(
        executionAutomation.id
      );


    const result =
      await runExecution(
        execution.id,
        submittedValues
      );


    /*
     * Clear runtime values immediately
     * after execution has returned.
     */
    setExecutionInputValues({});


    setSelectedExecution(
      result
    );


    if (selectedProject) {

      await loadProjectExecutions(
        selectedProject
      );

      await loadProjectQualitySummary(
        selectedProject
      );
    }


  } catch (err) {

    /*
     * Passwords/tokens must not remain
     * in React state following failure.
     */
    setExecutionInputValues({});

    setSelectedExecution(null);

    setError(
      err.message
    );


  } finally {

    /*
     * Clear temporary JS copy too.
     */
    for (
      const key of
      Object.keys(submittedValues)
    ) {
      submittedValues[key] = "";
    }


    setRunningTestCaseId(
      null
    );
  }
}

  async function handleViewScreenshot() {
  if (!selectedExecution) {
    return;
  }

  try {
    setScreenshotLoading(true);
    setError("");

    const screenshot =
      await getExecutionScreenshot(
        selectedExecution.id
      );

    if (!screenshot) {
      setError(
        "Screenshot evidence is not available."
      );

      return;
    }

    if (screenshotUrl) {
      URL.revokeObjectURL(
        screenshotUrl
      );
    }

    const objectUrl =
      URL.createObjectURL(
        screenshot
      );

    setScreenshotUrl(
      objectUrl
    );

  } catch (err) {
    setError(err.message);
  } finally {
    setScreenshotLoading(false);
  }
}

  async function handleDownloadTrace() {
  if (!selectedExecution) {
    return;
  }

  try {
    setError("");

    const trace =
      await getExecutionTrace(
        selectedExecution.id
      );

    if (!trace) {
      setError(
        "Playwright trace is not available."
      );

      return;
    }

    const objectUrl =
      URL.createObjectURL(trace);

    const link =
      document.createElement("a");

    link.href = objectUrl;

    link.download =
      `execution-${selectedExecution.id}-trace.zip`;

    document.body.appendChild(
      link
    );

    link.click();

    link.remove();

    URL.revokeObjectURL(
      objectUrl
    );

  } catch (err) {
    setError(err.message);
  }
}
  
  async function loadProjectExecutions(
  project
) {
  if (!project) {
    setProjectExecutions([]);
    return;
  }

  try {
    setExecutionsLoading(true);
    setError("");

    const executions =
      await getProjectExecutions(
        project.id
      );

    setProjectExecutions(
      executions
    );

  } catch (err) {
    setProjectExecutions([]);
    setError(err.message);
  } finally {
    setExecutionsLoading(false);
  }
}

  async function openExecutionsPage() {
  const project =
    selectedProject ||
    projects[0];

  if (!project) {
    setError(
      "No project is available for execution history."
    );

    return;
  }

  setSelectedProject(
    project
  );

  await loadProjectExecutions(
    project
  );

  setCurrentPage(
    "executions"
  );
}

  async function loadProjectQualitySummary(
  project
) {
  if (!project) {
    setProjectQualitySummary(null);
    return;
  }

  try {
    setReportsLoading(true);
    setError("");

    const summary =
      await getProjectQualitySummary(
        project.id
      );

    setProjectQualitySummary(
      summary
    );

  } catch (err) {
    setProjectQualitySummary(null);
    setError(err.message);
  } finally {
    setReportsLoading(false);
  }
}

  async function loadProjectCycleQualitySummary(
  project,
  filters = reportFilters
) {
  if (!project) {
    setProjectCycleQualitySummary(
      null
    );

    return;
  }


  try {

    setReportsLoading(
      true
    );

    setError("");


    const summary =
      await getProjectCycleQualitySummary(
  project.id,
  filters
);


    setProjectCycleQualitySummary(
      summary
    );


  } catch (err) {

    setProjectCycleQualitySummary(
      null
    );


    setError(
      err.message ||
      "Unable to load Cycle reporting."
    );


  } finally {

    setReportsLoading(
      false
    );
  }
}

  async function loadProjectCycleTraceability(
  project,
  filters = reportFilters
) {
  if (!project) {

    setProjectCycleTraceability(
      null
    );

    return;
  }


  try {

    setError("");


    const traceability =
      await getProjectCycleTraceability(
  project.id,
  filters
);


    setProjectCycleTraceability(
      traceability
    );


  } catch (err) {

    setProjectCycleTraceability(
      null
    );


    setError(
      err.message ||
      "Unable to load Cycle traceability."
    );
  }
}


  async function loadRequirementCoverage(
  project
) {
  if (!project) {
    setRequirementCoverage([]);
    return;
  }

  try {
    const coverage =
      await getRequirementCoverage(
        project.id
      );

    setRequirementCoverage(
      coverage
    );

  } catch (err) {
    setRequirementCoverage([]);
    setError(err.message);
  }
}

  async function applyReportFilters(
  filters
) {
  const project =
    selectedProject ||
    projects[0];


  if (!project) {

    setError(
      "No Project is available for reporting."
    );

    return;
  }


  const nextFilters = {
    release:
      String(
        filters?.release || ""
      ).trim(),

    environment:
      String(
        filters?.environment || ""
      ).trim(),

    cycle_status:
      filters?.cycle_status || "",

    result_status:
      filters?.result_status || "",

    execution_mode:
      filters?.execution_mode || ""
  };


  try {

    setReportFiltersLoading(
      true
    );

    setError("");


    const [
      cycleQuality,
      cycleTraceability,
      releaseQuality
    ] = await Promise.all([

      getProjectCycleQualitySummary(
        project.id,
        nextFilters
      ),


      getProjectCycleTraceability(
        project.id,
        nextFilters
      ),


      nextFilters.release
        ? getProjectReleaseQuality(
            project.id,
            nextFilters.release,
            nextFilters.environment
          )
        : Promise.resolve(
            null
          )

    ]);


    setReportFilters(
      nextFilters
    );


    setProjectCycleQualitySummary(
      cycleQuality
    );


    setProjectCycleTraceability(
      cycleTraceability
    );


    setProjectReleaseQuality(
      releaseQuality
    );


  } catch (err) {

    setProjectReleaseQuality(
      null
    );


    setError(
      err.message ||
      "Unable to apply report filters."
    );


  } finally {

    setReportFiltersLoading(
      false
    );
  }
}

  async function resetReportFilters() {
    const emptyFilters = {
    release: "",
    environment: "",
    cycle_status: "",
    result_status: "",
    execution_mode: ""
  };


  await applyReportFilters(
    emptyFilters
  );
}

  async function handleDownloadReleasePdf() {
  const project =
    selectedProject ||
    projects[0];


  const release =
    reportFilters?.release ||
    "";


  const environment =
    reportFilters?.environment ||
    "";


  if (
    !project ||
    !release
  ) {

    setError(
      "Select and apply a Release before downloading the report."
    );

    return;
  }


  try {

    setReleasePdfDownloading(
      true
    );


    setError("");


    const {
      blob,
      filename
    } =
      await downloadProjectReleaseQualityPdf(
        project.id,
        release,
        environment
      );


    const objectUrl =
      window.URL.createObjectURL(
        blob
      );


    const link =
      document.createElement(
        "a"
      );


    link.href =
      objectUrl;


    link.download =
      filename;


    document.body.appendChild(
      link
    );


    link.click();


    document.body.removeChild(
      link
    );


    window.URL.revokeObjectURL(
      objectUrl
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to download Release Quality PDF."
    );


  } finally {

    setReleasePdfDownloading(
      false
    );
  }
}

  async function handleDownloadReleaseExcel() {
  const project =
    selectedProject ||
    projects[0];


  const release =
    reportFilters?.release ||
    "";


  const environment =
    reportFilters?.environment ||
    "";


  if (
    !project ||
    !release
  ) {

    setError(
      "Select and apply a Release before downloading the Excel report."
    );

    return;
  }


  try {

    setReleaseExcelDownloading(
      true
    );


    setError("");


    const {
      blob,
      filename
    } =
      await downloadProjectReleaseQualityExcel(
        project.id,
        release,
        environment
      );


    const objectUrl =
      window.URL.createObjectURL(
        blob
      );


    const link =
      document.createElement(
        "a"
      );


    link.href =
      objectUrl;


    link.download =
      filename;


    document.body.appendChild(
      link
    );


    link.click();


    document.body.removeChild(
      link
    );


    window.URL.revokeObjectURL(
      objectUrl
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to download Release Quality Excel report."
    );


  } finally {

    setReleaseExcelDownloading(
      false
    );
  }
}

  async function openReportsPage() {
  const project =
    selectedProject ||
    projects[0];


  if (!project) {

    setError(
      "No project is available for reporting."
    );

    return;
  }


  const initialFilters = {
    release: "",
    environment: "",
    cycle_status: "",
    result_status: "",
    execution_mode: ""
  };


  setSelectedProject(
    project
  );

  setReportFilters(
    initialFilters
  );

  setProjectReleaseQuality(
    null
  );

  setReportsLoading(
    true
  );

  setError("");


  try {

    await Promise.all([
      loadProjectQualitySummary(
        project
      ),

      loadProjectCycleTraceability(
        project,
        initialFilters
      ),

      loadRequirementCoverage(
        project
      ),

      loadProjectExecutions(
        project
      ),

      loadProjectCycleQualitySummary(
        project,
        initialFilters
      )
    ]);


    setCurrentPage(
      "reports"
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to load Project reports."
    );


  } finally {

    setReportsLoading(
      false
    );
  }
}

  function handleViewHistoryExecution(
  execution
) {
  setFailureAnalysis(
  null
);

setFailureAnalysisError(
  ""
);

setFailureAnalysisLoading(
  false
);

  if (historyScreenshotUrl) {
    URL.revokeObjectURL(
      historyScreenshotUrl
    );
  }

  setHistoryScreenshotUrl(null);

  setSelectedHistoryExecution(
    execution
  );

  setShowExecutionDetailsModal(
    true
  );
}

  async function handleViewHistoryScreenshot() {
  if (!selectedHistoryExecution) {
    return;
  }

  try {
    setHistoryScreenshotLoading(
      true
    );

    setError("");

    const screenshot =
      await getExecutionScreenshot(
        selectedHistoryExecution.id
      );

    if (!screenshot) {
      setError(
        "Screenshot evidence is not available."
      );

      return;
    }

    if (historyScreenshotUrl) {
      URL.revokeObjectURL(
        historyScreenshotUrl
      );
    }

    const objectUrl =
      URL.createObjectURL(
        screenshot
      );

    setHistoryScreenshotUrl(
      objectUrl
    );

  } catch (err) {
    setError(err.message);
  } finally {
    setHistoryScreenshotLoading(
      false
    );
  }
}

 async function handleDownloadHistoryTrace() {
  if (!selectedHistoryExecution) {
    return;
  }

  try {
    setError("");

    const trace =
      await getExecutionTrace(
        selectedHistoryExecution.id
      );

    if (!trace) {
      setError(
        "Playwright trace is not available."
      );

      return;
    }

    const objectUrl =
      URL.createObjectURL(
        trace
      );

    const link =
      document.createElement("a");

    link.href = objectUrl;

    link.download =
      `execution-${selectedHistoryExecution.id}-trace.zip`;

    document.body.appendChild(
      link
    );

    link.click();
    link.remove();

    URL.revokeObjectURL(
      objectUrl
    );

  } catch (err) {
    setError(err.message);
  }
}

 function handleCloseExecutionDetails() {
  if (historyScreenshotUrl) {
    URL.revokeObjectURL(
      historyScreenshotUrl
    );
  }

  setHistoryScreenshotUrl(null);

  setShowExecutionDetailsModal(
    false
  );

  setSelectedHistoryExecution(
    null
  );
  setFailureAnalysis(
  null
);

setFailureAnalysisError(
  ""
);

setFailureAnalysisLoading(
  false
);
}

  async function handleAnalyzeExecutionFailure() {
  const execution =
    selectedHistoryExecution;


  if (!execution) {

    setFailureAnalysisError(
      "No Execution is selected."
    );

    return;
  }


  const status = String(
    execution.status ||
    ""
  ).trim().toLowerCase();


  if (
    status !== "failed" &&
    status !== "error"
  ) {

    setFailureAnalysisError(
      "AI failure analysis is available only for FAILED or ERROR executions."
    );

    return;
  }


  try {

    setFailureAnalysisLoading(
      true
    );


    setFailureAnalysisError(
      ""
    );


    setFailureAnalysis(
      null
    );


    const result =
      await analyzeExecutionFailure(
        execution.id
      );


    setFailureAnalysis(
      result
    );


  } catch (err) {

    setFailureAnalysis(
      null
    );


    setFailureAnalysisError(
      err.message ||
      "Unable to analyze the Execution failure."
    );


  } finally {

    setFailureAnalysisLoading(
      false
    );
  }
}

  async function loadAutomationHistory(
  testCaseId
) {
  try {

    setAutomationHistoryLoading(
      true
    );

    setError("");


    const history =
      await getAutomationHistory(
        testCaseId
      );


    setAutomationHistory(
      history
    );


  } catch (err) {

    setAutomationHistory([]);

    setError(
      err.message ||
      "Unable to load automation history."
    );


  } finally {

    setAutomationHistoryLoading(
      false
    );
  }
}

  async function handleViewAutomation(
  testCase
) {
  try {

    setLoadingAutomationId(
      testCase.id
    );

    setError("");


    const automation =
      await getTestCaseAutomation(
        testCase.id
      );


    if (!automation) {

      setError(
        "No automation exists for "
        + "this test case."
      );

      return;
    }


    setSelectedAutomationTestCase(
      testCase
    );

    setSelectedAutomation(
      automation
    );
    await loadAutomationHistory(
  testCase.id
);


    setAutomationByTestCase(
      (current) => ({
        ...current,
        [testCase.id]: automation
      })
    );


    setShowAutomationModal(
      true
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to load automation."
    );


  } finally {

    setLoadingAutomationId(
      null
    );
  }
}
  async function handleSaveAutomationEdit(
  code,
  changeSummary
) {
  if (
    !selectedAutomation ||
    !selectedAutomationTestCase
  ) {
    return;
  }


  const sourceAutomationId =
    selectedAutomation.id;


  const testCaseId =
    selectedAutomationTestCase.id;


  try {

    setSavingAutomationEditId(
      sourceAutomationId
    );

    setError("");


    const newAutomation =
      await createHumanEditedAutomation(
        sourceAutomationId,
        code,
        changeSummary
      );


    /*
     * Display the newly created DRAFT
     * version in the open Viewer.
     */
    setSelectedAutomation(
      newAutomation
    );


    /*
     * Store the automation using the
     * Test Case database ID as the key.
     *
     * Example:
     * {
     *   30: newAutomation
     * }
     */
    setAutomationByTestCase(
      (current) => ({
        ...current,
        [selectedAutomationTestCase.id]: newAutomation
      })
    );


    await loadAutomationHistory(
      testCaseId
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to save automation edit."
    );


  } finally {

    setSavingAutomationEditId(
      null
    );
  }
}

  async function handleUpdateAutomationWithAI(
  instruction
) {
  if (
    !selectedAutomation ||
    !selectedAutomationTestCase
  ) {
    return;
  }


  const sourceAutomationId =
    selectedAutomation.id;


  const testCaseId =
    selectedAutomationTestCase.id;


  try {

    setUpdatingAutomationWithAIId(
      sourceAutomationId
    );

    setError("");


    const newAutomation =
      await createAIUpdatedAutomation(
        sourceAutomationId,
        instruction
      );


    /*
     * Switch the Viewer to the newly
     * created AI_UPDATED DRAFT version.
     */
    setSelectedAutomation(
      newAutomation
    );


    /*
     * Update the Automation Workspace
     * entry for this exact Test Case.
     */
    setAutomationByTestCase(
      (current) => ({
        ...current,
        [selectedAutomationTestCase.id]:newAutomation
      })
    );


    await loadAutomationHistory(
      testCaseId
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to update automation with AI."
    );


  } finally {

    setUpdatingAutomationWithAIId(
      null
    );
  }
}

  async function handleReviewAutomation(
  status
) {
  if (
    !selectedAutomation ||
    !selectedAutomationTestCase
  ) {
    return;
  }


  const automationId =
    selectedAutomation.id;


  const testCaseId =
    selectedAutomationTestCase.id;


  try {

    setReviewingAutomationId(
      automationId
    );

    setError("");


    const updatedAutomation =
      await reviewAutomation(
        automationId,
        status
      );


    setSelectedAutomation(
      updatedAutomation
    );


    /*
     * Replace the Automation Workspace
     * entry for this exact Test Case.
     */
    setAutomationByTestCase(
      (current) => ({
        ...current,
       [selectedAutomationTestCase.id]: updatedAutomation
      })
    );
 

    await loadAutomationHistory(
      testCaseId
    );


    if (selectedProject) {

      await loadProjectQualitySummary(
        selectedProject
      );
    }


  } catch (err) {

    setError(
      err.message ||
      "Automation review failed."
    );


  } finally {

    setReviewingAutomationId(
      null
    );
  }
}

  async function loadAutomationWorkspace() {
  const eligibleTests =
  workspaceTestCases.filter(
    (testCase) => {

      const executionType =
        (
          testCase.execution_type ||
          "manual"
        ).toLowerCase();


      return (
        testCase.review_status ===
          "approved" &&
        (
          executionType ===
            "automation" ||
          executionType ===
            "both"
        )
      );
    }
  );

  try {
    setError("");

    const automationEntries =
      await Promise.all(
        eligibleTests.map(
          async (testCase) => {
            const automation =
              await getTestCaseAutomation(
                testCase.id
              );

            return [
              testCase.id,
              automation
            ];
          }
        )
      );

    setAutomationByTestCase(
      Object.fromEntries(
        automationEntries
      )
    );

  } catch (err) {
    setError(err.message);
  }
}

  async function loadProjectTestCycles(
  projectId
) {
  if (!projectId) {
    setTestCycles([]);
    return;
  }


  try {

    setTestCyclesLoading(
      true
    );

    setError("");


    const cycles =
      await getProjectTestCycles(
        projectId
      );


    setTestCycles(
      Array.isArray(cycles)
        ? cycles
        : []
    );


  } catch (err) {

    setTestCycles([]);

    setError(
      err.message ||
      "Unable to load Test Cycles."
    );


  } finally {

    setTestCyclesLoading(
      false
    );
  }
}

  async function loadCycleReadiness(
  projectId
) {
  if (!projectId) {
    setCycleReadiness(null);
    return null;
  }


  try {

    setCycleReadinessLoading(
      true
    );

    setError("");


    const readiness =
      await getProjectCycleReadiness(
        projectId
      );


    setCycleReadiness(
      readiness
    );


    return readiness;


  } catch (err) {

    setCycleReadiness(null);

    setError(
      err.message ||
      "Unable to load Cycle readiness."
    );


    return null;


  } finally {

    setCycleReadinessLoading(
      false
    );
  }
}

 async function openAutomationPage() {
  setCurrentPage("automation");

  await loadAutomationWorkspace();
}

  async function openTestCyclesPage() {
  if (!selectedProject) {

    setError(
      "Open a Project before viewing Test Cycles."
    );

    return;
  }


  setCurrentPage(
    "test-cycles"
  );


  setSelectedCycle(
    null
  );


  await loadProjectTestCycles(
    selectedProject.id
  );
}

  async function openCreateTestCycle() {
  if (!selectedProject) {

    setError(
      "Open a Project before creating a Test Cycle."
    );

    return;
  }


  resetCycleForm();


  setSelectedCycle(
    null
  );


  setShowCycleBuilder(
    true
  );


  await loadCycleReadiness(
    selectedProject.id
  );
}

  function closeCycleBuilder() {
  if (creatingTestCycle) {
    return;
  }


  setShowCycleBuilder(
    false
  );


  resetCycleForm();
}

  async function handleOpenTestCycle(
  cycle
) {
  if (!cycle?.id) {
    return;
  }


  try {

    setSelectedCycleLoading(
      true
    );

    setError("");


    const [
      detail,
      summary
    ] = await Promise.all([
      getTestCycle(
        cycle.id
      ),

      getTestCycleSummary(
        cycle.id
      )
    ]);


    setSelectedCycle(
      detail
    );


    setCycleSummary(
      summary
    );


    setCurrentPage(
      "cycle-workspace"
    );


  } catch (err) {

    setSelectedCycle(
      null
    );

    setCycleSummary(
      null
    );

    setError(
      err.message ||
      "Unable to load Test Cycle."
    );


  } finally {

    setSelectedCycleLoading(
      false
    );
  }
}

  async function refreshSelectedCycle() {
  if (!selectedCycle?.id) {
    return;
  }


  try {

    setSelectedCycleLoading(
      true
    );

    setError("");


    const [
      detail,
      summary
    ] = await Promise.all([
      getTestCycle(
        selectedCycle.id
      ),

      getTestCycleSummary(
        selectedCycle.id
      )
    ]);


    setSelectedCycle(
      detail
    );


    setCycleSummary(
      summary
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to refresh Test Cycle."
    );


  } finally {

    setSelectedCycleLoading(
      false
    );
  }
}

  async function handleCycleStatusChange(
  status
) {
  if (!selectedCycle?.id) {
    return;
  }


  try {

    setCycleActionLoading(
      true
    );

    setError("");


    const updated =
      await updateTestCycleStatus(
        selectedCycle.id,
        status
      );


    setSelectedCycle(
      updated
    );


    const updatedSummary =
      await getTestCycleSummary(
        selectedCycle.id
      );


    setCycleSummary(
      updatedSummary
    );


    if (selectedProject) {
      await loadProjectTestCycles(
        selectedProject.id
      );
    }


  } catch (err) {

    setError(
      err.message ||
      "Unable to update Test Cycle status."
    );


  } finally {

    setCycleActionLoading(
      false
    );
  }
}

  function resetManualResultForm() {
  setManualResultForm({
    status: "passed",
    actual_result: "",
    comment: "",
    defect_reference: ""
  });
}


function openManualCycleResult(
  item
) {
  setSelectedManualCycleItem(
    item
  );


  setManualResultForm({
    status:
      item.status &&
      item.status !== "not_run"
        ? item.status
        : "passed",

    actual_result:
      item.actual_result ||
      "",

    comment:
      item.comment ||
      "",

    defect_reference:
      item.defect_reference ||
      ""
  });


  setShowManualResultModal(
    true
  );
}


function closeManualCycleResult() {
  if (manualResultSaving) {
    return;
  }


  setShowManualResultModal(
    false
  );

  setSelectedManualCycleItem(
    null
  );

  resetManualResultForm();
}


function handleManualResultFormChange(
  event
) {
  const {
    name,
    value
  } = event.target;


  setManualResultForm(
    (current) => ({
      ...current,
      [name]: value
    })
  );
}

  async function handleManualResultSubmit(
  event
) {
  event.preventDefault();


  if (!selectedManualCycleItem) {
    return;
  }


  try {

    setManualResultSaving(
      true
    );

    setError("");


    await updateManualCycleResult(
      selectedManualCycleItem.id,
      {
        status:
          manualResultForm.status,

        actual_result:
          manualResultForm.actual_result
            .trim() || null,

        comment:
          manualResultForm.comment
            .trim() || null,

        defect_reference:
          manualResultForm
            .defect_reference
            .trim() || null
      }
    );


    setShowManualResultModal(
      false
    );

    setSelectedManualCycleItem(
      null
    );

    resetManualResultForm();


    await refreshSelectedCycle();


  } catch (err) {

    setError(
      err.message ||
      "Unable to save Manual result."
    );


  } finally {

    setManualResultSaving(
      false
    );
  }
}

  async function handlePrepareCycleAutomation(
  item
) {
  try {

    setPreparingCycleAutomationItemId(
      item.id
    );

    setError("");


    const schema =
      await getCycleAutomationInputs(
        item.id
      );


    const initialValues = {};


    for (
      const input of
      schema.inputs || []
    ) {
      initialValues[
        input.key
      ] =
        input.input_type ===
          "boolean"
          ? false
          : "";
    }


    setSelectedAutomationCycleItem(
      item
    );

    setCycleAutomationSchema(
      schema
    );

    setCycleAutomationValues(
      initialValues
    );

    setShowCycleAutomationModal(
      true
    );


  } catch (err) {

    setSelectedAutomationCycleItem(
      null
    );

    setCycleAutomationSchema(
      null
    );

    setCycleAutomationValues(
      {}
    );

    setError(
      err.message ||
      "Unable to prepare Cycle automation."
    );


  } finally {

    setPreparingCycleAutomationItemId(
      null
    );
  }
}

  function handleCycleAutomationInputChange(
  input,
  event
) {
  const value =
    input.input_type ===
      "boolean"
      ? event.target.checked
      : event.target.value;


  setCycleAutomationValues(
    (current) => ({
      ...current,
      [input.key]: value
    })
  );
}


function closeCycleAutomationModal() {
  if (
    runningCycleAutomationItemId !==
    null
  ) {
    return;
  }


  setShowCycleAutomationModal(
    false
  );

  setSelectedAutomationCycleItem(
    null
  );

  setCycleAutomationSchema(
    null
  );

  setCycleAutomationValues(
    {}
  );
}

  async function handleRunCycleAutomation(
  event
) {
  event.preventDefault();


  if (
    !selectedAutomationCycleItem ||
    !cycleAutomationSchema
  ) {
    return;
  }


  const submittedValues = {
    ...cycleAutomationValues
  };


  try {

    setRunningCycleAutomationItemId(
      selectedAutomationCycleItem.id
    );

    setError("");


    await runCycleAutomation(
      selectedAutomationCycleItem.id,
      submittedValues
    );


    setCycleAutomationValues(
      {}
    );

    setShowCycleAutomationModal(
      false
    );

    setSelectedAutomationCycleItem(
      null
    );

    setCycleAutomationSchema(
      null
    );


    await refreshSelectedCycle();


  } catch (err) {

    setCycleAutomationValues(
      {}
    );

    setError(
      err.message ||
      "Cycle automation execution failed."
    );


  } finally {

    for (
      const key of
      Object.keys(submittedValues)
    ) {
      submittedValues[key] = "";
    }


    setRunningCycleAutomationItemId(
      null
    );
  }
}

  async function handleOpenCycleExecution(
  item
) {
  if (!item?.execution_id) {
    return;
  }


  try {

    setError("");


    const execution =
      await getExecution(
        item.execution_id
      );


    handleViewHistoryExecution(
      execution
    );


  } catch (err) {

    setError(
      err.message ||
      "Unable to load Cycle Execution."
    );
  }
}

  const latestProject = projects.length > 0 ? projects[0] : null;

  return (
    <div className="app">
      <Sidebar
        currentPage={currentPage}
        onNavigate={setCurrentPage}
        onOpenRequirements={openRequirementsPage}
        onOpenTestCases={openTestCasesPage}
        onOpenAutomation={openAutomationPage}
        onOpenTestCycles={openTestCyclesPage}
        onOpenExecutions={openExecutionsPage}
        onOpenReports={openReportsPage}
      />

      <main className="main">
        {loading && (
          <div className="api-status">Loading QualiAgent data...</div>
        )}

        {error && <div className="api-error">{error}</div>}

        <Topbar currentPage={currentPage} selectedProject={selectedProject} />

        {currentPage === "dashboard" && (
          <DashboardPage
  projects={projects}
  requirements={requirements}
  testCases={testCases}
  latestProject={latestProject}
  qualitySummary={
    dashboardQualitySummary
  }
  onOpenProject={
    openProject
  }
  onOpenTestCases={
    openTestCasesPage
  }
  onOpenAutomation={
    openAutomationPage
  }
  onOpenExecutions={
    openExecutionsPage
  }
  onOpenReports={
    openReportsPage
  }
/>
        )}

        {currentPage === "projects" && (
          <ProjectsPage
            projects={projects}
            onCreateProject={() => {
              setError("");

              setProjectForm({
  name: "",
  description: "",
  application_type: "web",
  automation_engine: "playwright",
  automation_language: "javascript",
  default_browser: "chromium",
});

              setShowProjectForm(true);
            }}
            onOpenProject={openProject}
          />
        )}

        {(currentPage === "workspace" || currentPage === "requirements") && selectedProject && 
        (
          <ProjectWorkspacePage
            project={selectedProject}
            requirements={workspaceRequirements}
            testCases={workspaceTestCases}
            loading={workspaceLoading}
            analysingRequirementId={analysingRequirementId}
            getRequirementTestCount={getRequirementTestCount}
            scenarios={workspaceScenarios}
            scenariosLoading={scenariosLoading}
            getRequirementScenarioCount={getRequirementScenarioCount}
            getRequirementAIScenarioCount={getRequirementAIScenarioCount}
            onViewScenarios={handleViewScenarios}
            generatingScenariosRequirementId={generatingScenariosRequirementId}
            onGenerateScenarios={handleGenerateScenarios}
            onBack={() => setCurrentPage("projects")}
            onViewTestCases={openTestCasesPage}
            onAddRequirement={() => {
              setRequirementForm({
                requirement_id: "",
                title: "",
                description: "",
                application_type: selectedProject.application_type,
              });

              setError("");

              setShowRequirementForm(true);
            }}
            onAnalyseRequirement={handleAnalyseRequirement}
          />
        )}

        {currentPage === "scenarios" &&
  selectedProject &&
  selectedRequirement && (

  <ScenariosPage
  project={
    selectedProject
  }
  requirement={
    selectedRequirement
  }
  scenarios={
    workspaceScenarios
  }
  scenarioTestCases={
    scenarioTestCases
  }
  loading={
    scenariosLoading
  }
  generatingScenarioTestCasesId={
    generatingScenarioTestCasesId
  }
  onGenerateTestCases={
    handleGenerateScenarioTestCases
  }
  onBack={() =>
    setCurrentPage(
      "workspace"
    )
  }
  onOpenTestCase={
    openTestCase
  }
/>

)}

        {currentPage === "test-cases" && (
          <TestCasesPage
            project={selectedProject}
            requirements={workspaceRequirements}
            testCases={workspaceTestCases}
            loading={workspaceLoading}
            updatingTestCaseId={updatingTestCaseId}
            onBack={() => setCurrentPage("workspace")}
            onOpenTestCase={openTestCase}
          />
        )}

        {currentPage === "automation" && selectedProject && (
          <AutomationPage
  project={
    selectedProject
  }
  testCases={
    workspaceTestCases
  }
  automationByTestCase={
    automationByTestCase
  }
  loadingAutomationId={
    loadingAutomationId
  }
  preparingAutomationId={
    preparingAutomationId
  }
  onPrepareAutomation={
    handlePrepareAutomation
  }
  onViewAutomation={
    handleViewAutomation
  }
  onRunTest={
    handleOpenRunTest
  }
  onBack={() =>
    setCurrentPage(
      "workspace"
    )
  }
/>
        )}

        {currentPage ===
  "test-cycles" && (

  <TestCyclesPage
    project={
      selectedProject
    }

    cycles={
      testCycles
    }

    loading={
      testCyclesLoading
    }

    onCreateCycle={
      openCreateTestCycle
    }

    onOpenCycle={
      handleOpenTestCycle
    }

    onBack={() =>
  setCurrentPage(
    "workspace"
  )
}
  />

)}

        {currentPage ===
  "cycle-workspace" && (

  <CycleWorkspacePage
    cycle={
      selectedCycle
    }

    summary={
      cycleSummary
    }

    loading={
      selectedCycleLoading
    }

    actionLoading={
      cycleActionLoading
    }

    runningItemId={
      preparingCycleAutomationItemId ||
      runningCycleAutomationItemId
    }

    onBack={() => {

      setCurrentPage(
        "test-cycles"
      );


      setSelectedCycle(
        null
      );


      setCycleSummary(
        null
      );


      if (selectedProject) {

        loadProjectTestCycles(
          selectedProject.id
        );
      }
    }}

    onRefresh={
      refreshSelectedCycle
    }

    onChangeStatus={
      handleCycleStatusChange
    }

    onOpenManualResult={
      openManualCycleResult
    }

    onRunAutomation={
      handlePrepareCycleAutomation
    }

    onOpenExecution={
      handleOpenCycleExecution
    }
  />

)}

        {currentPage ===
  "test-cycles" &&
  selectedCycle && (

  <div className="api-status">

    Loaded Cycle:
    {" "}
    {selectedCycle.name}
    {" "}
    (
    {selectedCycle.items?.length || 0}
    {" "}
    items
    )

  </div>

)}

        {currentPage === "executions" &&
  selectedProject && (

  <ExecutionsPage
    project={
      selectedProject
    }
    executions={
      projectExecutions
    }
    loading={
      executionsLoading
    }
    onBack={() =>
      setCurrentPage(
        "workspace"
      )
    }
    onViewExecution={
      handleViewHistoryExecution
    }
  />

)}

        {currentPage === "reports" &&
  selectedProject && (

  <ReportsPage
    project={
      selectedProject
    }

    summary={
      projectQualitySummary
    }

    cycleSummary={
      projectCycleQualitySummary
    }

    releaseQuality={
      projectReleaseQuality
    }

    releasePdfDownloading={
  releasePdfDownloading
}

   onDownloadReleasePdf={
  handleDownloadReleasePdf
}

    releaseExcelDownloading={
  releaseExcelDownloading
}

    onDownloadReleaseExcel={
  handleDownloadReleaseExcel
}

    traceability={
      projectCycleTraceability
    }

    filters={
      reportFilters
    }

    filterOptions={
      projectCycleQualitySummary
        ?.filter_options
    }

    filtersLoading={
      reportFiltersLoading
    }

    onApplyFilters={
      applyReportFilters
    }

    onResetFilters={
      resetReportFilters
    }

    coverage={
      requirementCoverage
    }

    executions={
      projectExecutions
    }

    loading={
      reportsLoading
    }

    onViewExecution={
      handleViewHistoryExecution
    }

    onBack={() =>
      setCurrentPage(
        "workspace"
      )
    }
  />

)}

        {showCycleBuilder &&
  selectedProject && (

  <div className="modal-backdrop">

    <div className="modal-card cycle-builder-modal">

      <div className="modal-header">

        <div>

          <span className="section-label">
            TEST CYCLE BUILDER
          </span>

          <h3>
            Create Test Cycle
          </h3>

          <p className="modal-subtitle">
            {selectedProject.name}
          </p>

        </div>


        <button
          type="button"
          className="modal-close"
          disabled={
            creatingTestCycle
          }
          onClick={
            closeCycleBuilder
          }
        >
          ×
        </button>

      </div>


      <form
        onSubmit={
          handleCreateTestCycle
        }
      >

        <div className="cycle-builder-fields">

          <div className="form-field">

            <label htmlFor="cycle-name">
              Cycle Name
            </label>

            <input
              id="cycle-name"
              name="name"
              type="text"
              required
              minLength="3"
              maxLength="200"
              value={
                cycleForm.name
              }
              onChange={
                handleCycleFormChange
              }
              placeholder={
                "e.g. Sprint 12 Regression"
              }
            />

          </div>


          <div className="form-field">

            <label htmlFor="cycle-release">
              Release
            </label>

            <input
              id="cycle-release"
              name="release"
              type="text"
              maxLength="100"
              value={
                cycleForm.release
              }
              onChange={
                handleCycleFormChange
              }
              placeholder="e.g. 2.4"
            />

          </div>


          <div className="form-field">

            <label htmlFor="cycle-environment">
              Environment
            </label>

            <input
              id="cycle-environment"
              name="environment"
              type="text"
              maxLength="100"
              value={
                cycleForm.environment
              }
              onChange={
                handleCycleFormChange
              }
              placeholder={
                "e.g. QA"
              }
            />

          </div>

        </div>


        <div className="cycle-builder-summary">

          <span>
            Selected Test Cases
          </span>

          <strong>
            {
              getSelectedCycleItemCount()
            }
          </strong>

        </div>


        {cycleReadinessLoading ? (

          <div className="api-status">
            Loading Cycle readiness...
          </div>

        ) : !cycleReadiness ? (

          <div className="empty-state">

            <h4>
              Cycle readiness unavailable
            </h4>

            <p>
              QualiAgent could not load
              eligible Test Cases for this
              Project.
            </p>

          </div>

        ) : (
          cycleReadiness
            .requirements?.length ===
          0 ? (

            <div className="empty-state">

              <h4>
                No approved Test Cases
              </h4>

              <p>
                Approve and classify Test
                Cases before creating a
                Test Cycle.
              </p>

            </div>

          ) : (

            <div className="cycle-readiness-tree">

              {cycleReadiness
                .requirements
                .map(
                  (requirement) => (

                  <section
                    className="cycle-requirement"
                    key={
                      requirement.id
                    }
                  >

                    <div className="cycle-requirement-header">

                      <span className="requirement-id">
                        {
                          requirement
                            .requirement_id
                        }
                      </span>

                      <strong>
                        {
                          requirement
                            .title
                        }
                      </strong>

                    </div>


                    <div className="cycle-scenario-list">

                      {requirement
                        .scenarios
                        .map(
                          (scenario) => (

                          <section
                            className="cycle-scenario"
                            key={
                              scenario.id
                            }
                          >

                            <div className="cycle-scenario-header">

                              <span>
                                {
                                  scenario
                                    .scenario_id
                                }
                              </span>

                              <strong>
                                {
                                  scenario
                                    .title
                                }
                              </strong>

                            </div>


                            <div className="cycle-test-case-list">

                              {scenario
                                .test_cases
                                .map(
                                  (
                                    testCase
                                  ) => {

                                  const selection =
                                    cycleForm.items[
                                      testCase.id
                                    ];


                                  const selected =
                                    Boolean(
                                      selection
                                    );


                                  return (
                                    <article
                                      className={
                                        selected
                                          ? "cycle-test-case selected"
                                          : "cycle-test-case"
                                      }
                                      key={
                                        testCase.id
                                      }
                                    >

                                      <div className="cycle-test-case-main">

                                        <label className="cycle-test-select">

                                          <input
                                            type="checkbox"
                                            checked={
                                              selected
                                            }
                                            disabled={
                                              creatingTestCycle
                                            }
                                            onChange={
                                              (
                                                event
                                              ) =>
                                                handleCycleTestCaseSelection(
                                                  testCase,
                                                  event
                                                    .target
                                                    .checked
                                                )
                                            }
                                          />

                                          <span>

                                            <strong>
                                              {
                                                testCase
                                                  .test_case_id
                                              }
                                            </strong>

                                            <span>
                                              {
                                                testCase
                                                  .title
                                              }
                                            </span>

                                          </span>

                                        </label>


                                        <div className="cycle-test-case-tags">

                                          <span>
                                            {
                                              testCase
                                                .execution_type
                                                .toUpperCase()
                                            }
                                          </span>


                                          {testCase
                                            .automation_candidate && (

                                            <span>
                                              AI AUTOMATION CANDIDATE
                                            </span>

                                          )}


                                          {testCase
                                            .ready_automation && (

                                            <span>
                                              {
                                                testCase
                                                  .ready_automation
                                                  .engine
                                                  .toUpperCase()
                                              }
                                              {" "}
                                              V
                                              {
                                                testCase
                                                  .ready_automation
                                                  .version
                                              }
                                              {" "}
                                              READY
                                            </span>

                                          )}

                                        </div>

                                      </div>


                                      {selected && (

                                        <div className="cycle-execution-mode">

                                          <span>
                                            Run in this Cycle as:
                                          </span>


                                          <label>

                                            <input
                                              type="radio"
                                              name={
                                                `cycle-mode-${testCase.id}`
                                              }
                                              value="manual"
                                              checked={
                                                selection
                                                  .execution_mode ===
                                                "manual"
                                              }
                                              disabled={
                                                creatingTestCycle ||
                                                !testCase
                                                  .manual_eligible
                                              }
                                              onChange={() =>
                                                handleCycleExecutionMode(
                                                  testCase,
                                                  "manual"
                                                )
                                              }
                                            />

                                            Manual

                                          </label>


                                          <label>

                                            <input
                                              type="radio"
                                              name={
                                                `cycle-mode-${testCase.id}`
                                              }
                                              value="automation"
                                              checked={
                                                selection
                                                  .execution_mode ===
                                                "automation"
                                              }
                                              disabled={
                                                creatingTestCycle ||
                                                !testCase
                                                  .automation_eligible
                                              }
                                              onChange={() =>
                                                handleCycleExecutionMode(
                                                  testCase,
                                                  "automation"
                                                )
                                              }
                                            />

                                            Automation

                                          </label>


                                          {!testCase
                                            .automation_eligible &&
                                            (
                                              testCase
                                                .execution_type ===
                                                "automation" ||
                                              testCase
                                                .execution_type ===
                                                "both"
                                            ) && (

                                            <small>
                                              Automation unavailable:
                                              no compatible READY
                                              automation exists.
                                            </small>

                                          )}

                                        </div>

                                      )}

                                    </article>
                                  );
                                }
                              )}

                            </div>

                          </section>
                        )
                      )}

                    </div>

                  </section>
                )
              )}

            </div>

          )
        )}


        <div className="form-actions">

          <button
            type="button"
            className="secondary-button"
            disabled={
              creatingTestCycle
            }
            onClick={
              closeCycleBuilder
            }
          >
            Cancel
          </button>


          <button
            type="submit"
            className="primary-button"
            disabled={
              creatingTestCycle ||
              cycleReadinessLoading ||
              getSelectedCycleItemCount() ===
                0
            }
          >
            {
              creatingTestCycle
                ? "Creating Cycle..."
                : "Create Test Cycle"
            }
          </button>

        </div>

      </form>

    </div>

  </div>

)}

        {showManualResultModal &&
  selectedManualCycleItem && (

  <div className="modal-backdrop">

    <div className="modal-card cycle-result-modal">

      <div className="modal-header">

        <div>

          <span className="section-label">
            MANUAL EXECUTION
          </span>

          <h3>
            Record Manual Result
          </h3>

          <p className="modal-subtitle">
            Cycle Item #
            {selectedManualCycleItem.id}
          </p>

        </div>


        <button
          type="button"
          className="modal-close"
          disabled={
            manualResultSaving
          }
          onClick={
            closeManualCycleResult
          }
        >
          ×
        </button>

      </div>


      <form
        onSubmit={
          handleManualResultSubmit
        }
      >

        <div className="form-field">

          <label htmlFor="manual-result-status">
            Result
          </label>

          <select
            id="manual-result-status"
            name="status"
            value={
              manualResultForm.status
            }
            disabled={
              manualResultSaving
            }
            onChange={
              handleManualResultFormChange
            }
          >
            <option value="passed">
              Passed
            </option>

            <option value="failed">
              Failed
            </option>

            <option value="blocked">
              Blocked
            </option>

            <option value="skipped">
              Skipped
            </option>
          </select>

        </div>


        <div className="form-field">

          <label htmlFor="manual-actual-result">
            Actual Result
          </label>

          <textarea
            id="manual-actual-result"
            name="actual_result"
            rows="5"
            maxLength="5000"
            required={
              manualResultForm.status ===
              "failed"
            }
            disabled={
              manualResultSaving
            }
            value={
              manualResultForm
                .actual_result
            }
            onChange={
              handleManualResultFormChange
            }
            placeholder={
              "Describe the observed result."
            }
          />

          {manualResultForm.status ===
            "failed" && (

            <small>
              Actual Result is required for
              a failed Manual Test Case.
            </small>

          )}

        </div>


        <div className="form-field">

          <label htmlFor="manual-comment">
            Comment
          </label>

          <textarea
            id="manual-comment"
            name="comment"
            rows="3"
            maxLength="2000"
            required={
              manualResultForm.status ===
              "blocked"
            }
            disabled={
              manualResultSaving
            }
            value={
              manualResultForm.comment
            }
            onChange={
              handleManualResultFormChange
            }
            placeholder={
              "Add execution notes or a blocked reason."
            }
          />

          {manualResultForm.status ===
            "blocked" && (

            <small>
              Comment is required for a
              blocked Manual Test Case.
            </small>

          )}

        </div>


        <div className="form-field">

          <label htmlFor="manual-defect">
            Defect Reference
          </label>

          <input
            id="manual-defect"
            name="defect_reference"
            type="text"
            maxLength="200"
            disabled={
              manualResultSaving
            }
            value={
              manualResultForm
                .defect_reference
            }
            onChange={
              handleManualResultFormChange
            }
            placeholder={
              "e.g. JIRA-142"
            }
          />

        </div>


        <div className="form-actions">

          <button
            type="button"
            className="secondary-button"
            disabled={
              manualResultSaving
            }
            onClick={
              closeManualCycleResult
            }
          >
            Cancel
          </button>


          <button
            type="submit"
            className="primary-button"
            disabled={
              manualResultSaving
            }
          >
            {manualResultSaving
              ? "Saving..."
              : "Save Result"}
          </button>

        </div>

      </form>

    </div>

  </div>

)}

        {showCycleAutomationModal &&
  selectedAutomationCycleItem &&
  cycleAutomationSchema && (

  <div className="modal-backdrop">

    <div className="modal-card automation-input-modal">

      <div className="modal-header">

        <div>

          <span className="section-label">
            CYCLE AUTOMATION
          </span>

          <h3>
            Run Frozen Automation
          </h3>

          <p className="modal-subtitle">
            Cycle Item #
            {selectedAutomationCycleItem.id}
            {" · "}
            Automation #
            {
              selectedAutomationCycleItem
                .automation_version_id
            }
          </p>

        </div>


        <button
          type="button"
          className="modal-close"
          disabled={
            runningCycleAutomationItemId !==
            null
          }
          onClick={
            closeCycleAutomationModal
          }
        >
          ×
        </button>

      </div>


      <div className="analysis-notice">
        Runtime values are supplied only for
        this Cycle execution. Secret values
        are cleared from the form after the
        request and are not stored on the
        Cycle item.
      </div>


      <form
        onSubmit={
          handleRunCycleAutomation
        }
      >

        {(cycleAutomationSchema.inputs ||
          []).length === 0 ? (

          <div className="empty-state">

            <h4>
              No runtime inputs required
            </h4>

            <p>
              The frozen automation version
              can execute without
              tester-supplied values.
            </p>

          </div>

        ) : (

          <div className="automation-input-list">

            {cycleAutomationSchema.inputs.map(
              (input) => (

                <AutomationInputField
                  key={input.key}
                  input={input}
                  value={
                    cycleAutomationValues[
                      input.key
                    ]
                  }
                  disabled={
                    runningCycleAutomationItemId !==
                    null
                  }
                  onChange={
                    handleCycleAutomationInputChange
                  }
                />

              )
            )}

          </div>

        )}


        <div className="form-actions">

          <button
            type="button"
            className="secondary-button"
            disabled={
              runningCycleAutomationItemId !==
              null
            }
            onClick={
              closeCycleAutomationModal
            }
          >
            Cancel
          </button>


          <button
            type="submit"
            className="primary-button"
            disabled={
              runningCycleAutomationItemId !==
              null
            }
          >
            {runningCycleAutomationItemId !==
              null
              ? "Running..."
              : "Run Automation"}
          </button>

        </div>

      </form>

    </div>

  </div>

)}

        {showProjectForm && (
          <div className="modal-backdrop">
            <div className="modal-card">
              <div className="modal-header">
                <div>
                  <span className="section-label">NEW QA WORKSPACE</span>

                  <h3>Create Project</h3>
                </div>

                <button
                  type="button"
                  className="modal-close"
                  onClick={() => setShowProjectForm(false)}
                >
                  ×
                </button>
              </div>

              <form onSubmit={handleCreateProject}>
                <div className="form-field">
                  <label htmlFor="project-name">Project name</label>

                  <input
                    id="project-name"
                    name="name"
                    type="text"
                    minLength="3"
                    maxLength="200"
                    required
                    value={projectForm.name}
                    onChange={handleProjectChange}
                    placeholder={"e.g. Customer Portal QA"}
                  />
                </div>

                <div className="form-field">
                  <label htmlFor={"project-description"}>Description</label>

                  <textarea
                    id="project-description"
                    name="description"
                    minLength="5"
                    maxLength="1000"
                    required
                    value={projectForm.description}
                    onChange={handleProjectChange}
                    placeholder={"What are you testing?"}
                    rows="4"
                  />
                </div>

                <div className="form-field">

  <label>
    Application Type
  </label>

  <input
    type="text"
    value="Web"
    disabled
  />

  <small>
    QualiAgent currently supports
    web application QA projects.
  </small>

</div>
                
                <div className="form-field">

  <label
    htmlFor="automation-engine"
  >
    Automation Engine
  </label>

  <select
    id="automation-engine"
    name="automation_engine"
    value={
      projectForm.automation_engine
    }
    onChange={
      handleProjectChange
    }
  >
    <option value="playwright">
      Playwright
    </option>

    <option value="selenium">
      Selenium
    </option>
  </select>

  <small>
    Automation Test Cases generated
    in this project will use this engine.
  </small>

</div>

                <div className="form-field">

  <label
    htmlFor="automation-language"
  >
    Automation Language
  </label>

  <input
    id="automation-language"
    type="text"
    value={
      projectForm
        .automation_language ===
      "python"
        ? "Python"
        : "JavaScript"
    }
    disabled
  />

  <small>
    Language is currently selected
    automatically from the automation
    engine.
  </small>

</div>

                <div className="form-field">

  <label
    htmlFor="default-browser"
  >
    Default Browser
  </label>

  <select
    id="default-browser"
    name="default_browser"
    value={
      projectForm.default_browser
    }
    onChange={
      handleProjectChange
    }
  >
    <option value="chromium">
      Chromium
    </option>

    <option value="firefox">
      Firefox
    </option>

    <option value="webkit">
      WebKit
    </option>
  </select>

</div>

                <div className="form-actions">
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() => setShowProjectForm(false)}
                  >
                    Cancel
                  </button>

                  <button
                    type="submit"
                    className="primary-button"
                    disabled={savingProject}
                  >
                    {savingProject ? "Creating..." : "Create Project"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {showRequirementForm && selectedProject && (
          <div className="modal-backdrop">
            <div className="modal-card">
              <div className="modal-header">
                <div>
                  <span className="section-label">NEW REQUIREMENT</span>

                  <h3>Add Requirement</h3>
                </div>

                <button
                  type="button"
                  className="modal-close"
                  onClick={() => setShowRequirementForm(false)}
                >
                  ×
                </button>
              </div>

              <form onSubmit={handleCreateRequirement}>
                <div className="form-field">
                  <label htmlFor="requirement-id">Requirement ID</label>

                  <input
                    id="requirement-id"
                    name="requirement_id"
                    type="text"
                    minLength="1"
                    maxLength="50"
                    required
                    value={requirementForm.requirement_id}
                    onChange={handleRequirementChange}
                    placeholder={"e.g. REQ-003"}
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="requirement-title">Title</label>

                  <input
                    id="requirement-title"
                    name="title"
                    type="text"
                    minLength="3"
                    maxLength="200"
                    required
                    value={requirementForm.title}
                    onChange={handleRequirementChange}
                    placeholder={"e.g. Customer Checkout"}
                  />
                </div>

                <div className="form-field">
                  <label htmlFor={"requirement-description"}>Requirement</label>

                  <textarea
                    id={"requirement-description"}
                    name="description"
                    minLength="10"
                    maxLength="5000"
                    required
                    rows="6"
                    value={requirementForm.description}
                    onChange={handleRequirementChange}
                    placeholder={
                      "Describe the expected application behaviour..."
                    }
                  />
                </div>

                <div className="form-field">
                  <label htmlFor={"requirement-application"}>
                    Application type
                  </label>

                  <select
                    id={"requirement-application"}
                    name="application_type"
                    value={requirementForm.application_type}
                    onChange={handleRequirementChange}
                  >
                    <option value="web">Web</option>

                    <option value="mobile">Mobile</option>

                    <option value="api">API</option>
                  </select>
                </div>

                <div className="form-actions">
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() => setShowRequirementForm(false)}
                  >
                    Cancel
                  </button>

                  <button
                    type="submit"
                    className="primary-button"
                    disabled={savingRequirement}
                  >
                    {savingRequirement ? "Saving..." : "Add Requirement"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {showAnalysisModal && requirementAnalysis && selectedRequirement && (
          <div className="modal-backdrop">
            <div className="modal-card analysis-modal">
              <div className="modal-header">
                <div>
                  <span className="section-label">QA REQUIREMENT ANALYSIS</span>

                  <h3>{selectedRequirement.title}</h3>

                  <p className="modal-subtitle">
                    {selectedRequirement.requirement_id}
                  </p>
                </div>

                <button
                  type="button"
                  className="modal-close"
                  onClick={() => setShowAnalysisModal(false)}
                >
                  ×
                </button>
              </div>

              <div className="analysis-notice">
  Requirement analysis generated by
  QualiAgent AI. Review the analysis,
  acceptance criteria and clarification
  questions before continuing.
</div>

              <div className="analysis-summary">
                <AnalysisMetric
                  label="Testable"
                  value={requirementAnalysis.testable ? "Yes" : "No"}
                />

                <AnalysisMetric
                  label="Risk"
                  value={requirementAnalysis.risk_level.toUpperCase()}
                />

                <AnalysisMetric
                  label="Application"
                  value={requirementAnalysis.application_type.toUpperCase()}
                />
              </div>

              <AnalysisSection
  title="AI Summary"
  items={[
    requirementAnalysis.summary
  ]}
  emptyMessage={
    "No AI summary generated."
  }
/>

              <AnalysisSection
                title="Identified Keywords"
                items={requirementAnalysis.identified_keywords}
                emptyMessage={"No testing keywords identified."}
                compact
              />

              <AnalysisSection
                title="Suggested Test Types"
                items={requirementAnalysis.suggested_test_types}
                emptyMessage={"No test types suggested."}
                compact
              />

              <AnalysisSection
                title="Acceptance Criteria"
                items={requirementAnalysis.acceptance_criteria}
                emptyMessage={"No acceptance criteria generated."}
              />

              <AnalysisSection
                title="Clarification Questions"
                items={requirementAnalysis.questions}
                emptyMessage={"No clarification questions generated."}
              />

              <div className="analysis-footer">
                <span>
  AI-generated analysis. Human review
  is required before test design.
</span>

                <button
                  type="button"
                  className="primary-button"
                  onClick={() => setShowAnalysisModal(false)}
                >
                  Close Analysis
                </button>
              </div>
            </div>
          </div>
        )}

        {showTestCaseModal && selectedTestCase && (
          <div className="modal-backdrop">
            <div className="modal-card test-case-modal">
              <div className="modal-header">
                <div>
                  <span className="section-label">TEST CASE DETAILS</span>

                  <h3>{selectedTestCase.title}</h3>

                  <p className="modal-subtitle">
                    {selectedTestCase.test_case_id}
                  </p>
                </div>

                <button
                  type="button"
                  className="modal-close"
                  onClick={() => setShowTestCaseModal(false)}
                >
                  ×
                </button>
              </div>

              <div className="test-case-detail-tags">

  <span>
    {
      selectedTestCase
        .test_type
        .toUpperCase()
    }
  </span>


  <span>
    {
      selectedTestCase
        .priority
        .toUpperCase()
    }
    {" "}
    PRIORITY
  </span>


  {/* AI recommendation */}
  <span>
    {
      selectedTestCase
        .automation_candidate
        ? "AUTOMATION CANDIDATE"
        : "MANUAL CANDIDATE"
    }
  </span>


  {/* Human execution decision */}
  <span>
    {
      (
        selectedTestCase
          .execution_type ||
        "manual"
      ).toUpperCase()
    }
    {" "}
    EXECUTION
  </span>


  {/* Human Test Case review status */}
  <span
    className={
      `review-status review-${
        selectedTestCase
          .review_status ||
        "draft"
      }`
    }
  >
    {
      (
        selectedTestCase
          .review_status ||
        "draft"
      ).toUpperCase()
    }
  </span>

</div>

              <TestCaseDetailSection title="Requirement">
                <p>
                  {selectedTestCase.requirement_id}

                  {" · "}

                  {getRequirementTitle(selectedTestCase.requirement_db_id)}
                </p>
              </TestCaseDetailSection>

              <TestCaseDetailSection title="Preconditions">
                {(selectedTestCase.preconditions || []).length === 0 ? (
                  <p>No preconditions specified.</p>
                ) : (
                  <ul>
                    {(selectedTestCase.preconditions || []).map(
                      (precondition, index) => (
                        <li key={`${precondition}-${index}`}>{precondition}</li>
                      ),
                    )}
                  </ul>
                )}
              </TestCaseDetailSection>

              <TestCaseDetailSection title="Test Data">
                {(selectedTestCase.test_data || []).length === 0 ? (
                  <p>No test data specified.</p>
                ) : (
                  <ul>
                    {(selectedTestCase.test_data || []).map(
                      (dataItem, index) => (
                        <li key={`${dataItem}-${index}`}>{dataItem}</li>
                      ),
                    )}
                  </ul>
                )}
              </TestCaseDetailSection>

              <TestCaseDetailSection title="Test Steps">
                <div className="test-step-list">
                  {(selectedTestCase.steps || []).map((step) => (
                    <article
                      className={"test-step-card"}
                      key={step.step_number}
                    >
                      <div className={"test-step-number"}>
                        {step.step_number}
                      </div>

                      <div className={"test-step-content"}>
                        <strong>Action</strong>

                        <p>{step.action}</p>

                        <strong>Expected Result</strong>

                        <p>{step.expected_result}</p>
                      </div>
                    </article>
                  ))}
                </div>
              </TestCaseDetailSection>

              <TestCaseDetailSection
  title="Execution Classification"
>

  <div className="test-execution-classification">

    <div className="test-execution-recommendation">

      <span className="section-label">
        AI RECOMMENDATION
      </span>

      <strong>
        {selectedTestCase
          .automation_candidate
          ? "Automation Candidate"
          : "Manual Candidate"}
      </strong>

      <p>
        This is an AI/system suitability
        recommendation. The human QA
        decision below controls how this
        Test Case can later be selected
        into a Test Cycle.
      </p>

    </div>


    <div className="form-field">

      <label
        htmlFor="test-execution-type"
      >
        Human Execution Decision
      </label>


      <select
        id="test-execution-type"
        value={
          selectedTestCase
            .execution_type ||
          "manual"
        }
        disabled={
          selectedTestCase.review_status
            !== "approved" ||
          updatingExecutionTypeId ===
            selectedTestCase.id
        }
        onChange={(event) =>
          handleTestCaseExecutionType(
            selectedTestCase,
            event.target.value
          )
        }
      >

        <option value="manual">
          Manual
        </option>

        <option value="automation">
          Automation
        </option>

        <option value="both">
          Both
        </option>

      </select>


      <small>

        {selectedTestCase.review_status
          !== "approved"
          ? (
            "Approve this Test Case before "
            + "selecting its execution type."
          )
          : (
            "This classification does not "
            + "execute the Test Case. "
            + "Execution will be planned "
            + "inside a Test Cycle."
          )}

      </small>

    </div>


    {updatingExecutionTypeId ===
      selectedTestCase.id && (

      <div className="api-status">
        Saving execution classification...
      </div>

    )}

  </div>

</TestCaseDetailSection>

              <div className="test-review-footer">
                <div className="test-review-state">
                  <span>Review Status</span>

                  <strong>
                    {getReviewStatus(selectedTestCase).toUpperCase()}
                  </strong>
                </div>

                <div className="test-review-actions">
                  <button
                    type="button"
                    className="reject-button"
                    disabled={updatingTestCaseId === selectedTestCase.id}
                    onClick={() =>
                      handleTestCaseStatus(selectedTestCase, "rejected")
                    }
                  >
                    {updatingTestCaseId === selectedTestCase.id
                      ? "Updating..."
                      : "Reject"}
                  </button>

                  <button
                    type="button"
                    className="approve-button"
                    disabled={
  updatingTestCaseId ===
    selectedTestCase.id ||
  getReviewStatus(
    selectedTestCase
  ) === "approved"
}
                    onClick={() =>
                      handleTestCaseStatus(selectedTestCase, "approved")
                    }
                  >
                    {updatingTestCaseId ===
selectedTestCase.id
  ? "Updating..."
  : getReviewStatus(
      selectedTestCase
    ) === "approved"
    ? "Approved for Automation"
    : "Approve for Automation"}
                  </button>

                  <button
                    type="button"
                    className="secondary-button"
                    disabled={updatingTestCaseId === selectedTestCase.id}
                    onClick={() => setShowTestCaseModal(false)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

      {showAutomationModal &&
  selectedAutomation &&
  selectedAutomationTestCase && (

  <AutomationViewerModal
  automation={
    selectedAutomation
  }

  testCase={
    selectedAutomationTestCase
  }

  history={
  automationHistory
}

  historyLoading={
  automationHistoryLoading
}

  reviewing={
    reviewingAutomationId ===
    selectedAutomation.id
  }

  savingEdit={
    savingAutomationEditId ===
    selectedAutomation.id
  }

  onSaveEdit={
    handleSaveAutomationEdit
  }

  updatingWithAI={
  updatingAutomationWithAIId ===
  selectedAutomation.id
}

  onUpdateWithAI={
  handleUpdateAutomationWithAI
}

  onApprove={() =>
    handleReviewAutomation(
      "ready"
    )
  }

  onReject={() =>
    handleReviewAutomation(
      "rejected"
    )
  }

  onClose={() => {
    setShowAutomationModal(
      false
    );
  }}
/>

)}

      {showRunModal &&
  executionTestCase && (

  <div className="modal-backdrop">

    <div className="modal-card automation-input-modal">

      <div className="modal-header">

        <div>

          <span className="section-label">
            RUN AUTOMATION
          </span>

          <h3>
            {executionTestCase.title}
          </h3>

          <p className="modal-subtitle">
            {executionTestCase.test_case_id}
          </p>

        </div>


        <button
          type="button"
          className="modal-close"
          disabled={
            runningTestCaseId !== null
          }
          onClick={closeRunModal}
        >
          ×
        </button>

      </div>


      {preparingExecutionInputs ? (

        <div className="api-status">
          Preparing runtime inputs...
        </div>

      ) : !executionAutomation ? (

        <div>

          <div className="api-error">
            Unable to load READY automation
            for this Test Case.
          </div>

          <div className="form-actions">

            <button
              type="button"
              className="secondary-button"
              onClick={closeRunModal}
            >
              Close
            </button>

          </div>

        </div>

      ) : !executionInputSchema ? (

        <div>

          <div className="api-error">
            Unable to determine the runtime
            inputs required by this Test Case.
          </div>

          <div className="form-actions">

            <button
              type="button"
              className="secondary-button"
              onClick={closeRunModal}
            >
              Close
            </button>

          </div>

        </div>

      ) : !selectedExecution ? (

        <form
          onSubmit={(event) => {
            event.preventDefault();
            handleRunTest();
          }}
        >

          <div className="analysis-notice">
            Provide the runtime data required
            for this execution. Sensitive
            values are supplied only to the
            Playwright process for this run
            and cleared from the form
            afterwards.
          </div>


          {(executionInputSchema.inputs || [])
            .length === 0 ? (

            <div className="empty-state">

              <h4>
                No runtime inputs required
              </h4>

              <p>
                This automation does not
                require tester-supplied
                runtime data.
              </p>

            </div>

          ) : (

            <div className="automation-input-list">

              {executionInputSchema.inputs.map(
                (input) => (

                <AutomationInputField
                  key={input.key}
                  input={input}
                  value={
                    executionInputValues[
                      input.key
                    ]
                  }
                  disabled={
                    runningTestCaseId !== null
                  }
                  onChange={
                    handleExecutionInputChange
                  }
                />

              ))}

            </div>

          )}


          <div className="form-actions">

            <button
              type="button"
              className="secondary-button"
              disabled={
                runningTestCaseId !== null
              }
              onClick={closeRunModal}
            >
              Cancel
            </button>


            <button
              type="submit"
              className="primary-button"
              disabled={
                runningTestCaseId !== null
              }
            >
              {runningTestCaseId !== null
                ? "Running..."
                : "Run Test"}
            </button>

          </div>

        </form>

      ) : (

        <>

          <ExecutionResult
            execution={selectedExecution}
          />


          <div className="execution-evidence">

            <span className="section-label">
              EVIDENCE
            </span>


            <div className="execution-evidence-status">

              <span>
                Screenshot
              </span>

              <strong>
                {selectedExecution
                  .screenshot_path
                  ? "Available"
                  : "Not Available"}
              </strong>

            </div>


            <div className="execution-evidence-status">

              <span>
                Playwright Trace
              </span>

              <strong>
                {selectedExecution
                  .trace_path
                  ? "Available"
                  : "Not Available"}
              </strong>

            </div>


            <div className="execution-evidence-actions">

              {selectedExecution
                .screenshot_path && (

                <button
                  type="button"
                  className="secondary-button"
                  disabled={screenshotLoading}
                  onClick={handleViewScreenshot}
                >
                  {screenshotLoading
                    ? "Loading..."
                    : "View Screenshot"}
                </button>

              )}


              {selectedExecution
                .trace_path && (

                <button
                  type="button"
                  className="secondary-button"
                  onClick={handleDownloadTrace}
                >
                  Download Trace
                </button>

              )}

            </div>


            {screenshotUrl && (

              <div className="execution-screenshot">

                <img
                  src={screenshotUrl}
                  alt="Execution evidence"
                />

              </div>

            )}

          </div>


          <div className="form-actions">

            <button
              type="button"
              className="primary-button"
              onClick={closeRunModal}
            >
              Close
            </button>

          </div>

        </>

      )}

    </div>

  </div>

)}

  {showExecutionDetailsModal &&
  selectedHistoryExecution && (

  <ExecutionDetailsModal
    execution={
      selectedHistoryExecution
    }
    screenshotUrl={
      historyScreenshotUrl
    }
    screenshotLoading={
      historyScreenshotLoading
    }
    failureAnalysis={
  failureAnalysis
}

failureAnalysisLoading={
  failureAnalysisLoading
}

failureAnalysisError={
  failureAnalysisError
}

onAnalyzeFailure={
  handleAnalyzeExecutionFailure
}
    onViewScreenshot={
      handleViewHistoryScreenshot
    }
    onDownloadTrace={
      handleDownloadHistoryTrace
    }
    onClose={
      handleCloseExecutionDetails
    }
  />

)}

  {showAutomationInputModal &&
  automationInputSchema &&
  preparingAutomationTestCase && (

  <div className="modal-backdrop">

    <div className="modal-card automation-input-modal">

      <div className="modal-header">

        <div>

          <span className="section-label">
            AUTOMATION DATA
          </span>

          <h3>
            Prepare Automation
          </h3>

          <p className="modal-subtitle">
            {
              preparingAutomationTestCase
                .test_case_id
            }
          </p>

        </div>


        <button
  type="button"
  className="modal-close"
  disabled={
    generatingRealAutomationId !==
    null
  }
  onClick={
    closeAutomationInputModal
  }
>
  ×
</button>

      </div>


      <div className="automation-input-notice">
  Provide the runtime data required for
  this approved Test Case. Secret values
  are submitted only for this generation
  request and are cleared from the form
  afterwards.
</div>


      <form
        onSubmit={
          handleAutomationInputContinue
        }
      >

        {(automationInputSchema.inputs || [])
          .length === 0 ? (

          <div className="empty-state">

            <h4>
              No additional inputs required
            </h4>

            <p>
              QualiAgent AI determined that
              this Test Case does not require
              tester-supplied runtime data.
            </p>

          </div>

        ) : (

          <div className="automation-input-list">

            {automationInputSchema.inputs.map(
              (input) => (

              <AutomationInputField
                key={input.key}
                input={input}
                value={
                  automationInputValues[
                    input.key
                  ]
                }
                disabled={generatingRealAutomationId !==null}
                onChange={
                  handleAutomationInputChange
                }
              />

            ))}

          </div>

        )}


        <div className="form-actions">

          <button
  type="button"
  className="secondary-button"
  disabled={
    generatingRealAutomationId !==
    null
  }
  onClick={
    closeAutomationInputModal
  }
>
  Cancel
</button>

          <button
  type="submit"
  className="primary-button"
  disabled={
    generatingRealAutomationId !==
    null
  }
>
  {generatingRealAutomationId !==
  null
    ? "Generating Playwright..."
    : "Generate Automation"}
</button>

        </div>

      </form>

    </div>

  </div>

)}
      </main>
    </div>
  );
}

function AnalysisMetric({ label, value }) {
  return (
    <div className="analysis-metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function AnalysisSection({ title, items, emptyMessage, compact = false }) {
  const safeItems = Array.isArray(items) ? items : [];

  return (
    <section className="analysis-section">
      <h4>{title}</h4>

      {safeItems.length === 0 ? (
        <p className="analysis-empty">{emptyMessage}</p>
      ) : compact ? (
        <div className="analysis-tags">
          {safeItems.map((item, index) => (
            <span key={`${item}-${index}`}>{item}</span>
          ))}
        </div>
      ) : (
        <ul>
          {safeItems.map((item, index) => (
            <li key={`${item}-${index}`}>{item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}

function ExecutionResult({
  execution
}) {
  const status =
    execution.status ||
    "unknown";

  return (
    <div className="execution-result">

      <div
        className={
          `execution-status execution-${status}`
        }
      >
        {status.toUpperCase()}
      </div>


      <div className="execution-result-grid">

        <div>

          <span>
            Exit Code
          </span>

          <strong>
            {execution.exit_code ??
              "N/A"}
          </strong>

        </div>


        <div>

          <span>
            Duration
          </span>

          <strong>
            {execution.duration_ms !==
            null &&
            execution.duration_ms !==
            undefined
              ? `${execution.duration_ms} ms`
              : "N/A"}
          </strong>

        </div>

      </div>


      {execution.error_message && (

        <div className="api-error">
          {execution.error_message}
        </div>

      )}


      {execution.stdout && (

        <div className="execution-output">

          <strong>
            Playwright Output
          </strong>

          <pre>
            {execution.stdout}
          </pre>

        </div>

      )}

    </div>
  );
}

function AutomationInputField({
  input,
  value,
  disabled = false,
  onChange
}) {
  if (input.input_type === "boolean") {
    return (
      <div className="automation-input-field automation-input-checkbox">

        <label>

          <input
            type="checkbox"
            disabled={disabled}
            checked={Boolean(value)}
            onChange={(event) =>
              onChange(
                input,
                event
              )
            }
          />

          <span>
            {input.label}
          </span>

        </label>

        <small>
          {input.description}
        </small>

      </div>
    );
  }


  if (input.input_type === "textarea") {
    return (
      <div className="automation-input-field">

        <label
          htmlFor={
            `automation-${input.key}`
          }
        >
          {input.label}

          {input.required
            ? " *"
            : ""}
        </label>

        <textarea
          disabled={disabled}
          id={
            `automation-${input.key}`
          }
          rows="4"
          required={input.required}
          value={value ?? ""}
          placeholder={
            input.placeholder || ""
          }
          onChange={(event) =>
            onChange(
              input,
              event
            )
          }
        />

        <AutomationInputHelp
          input={input}
        />

      </div>
    );
  }


  const htmlType = {
    password: "password",
    url: "url",
    number: "number",
    email: "email",
    text: "text"
  }[input.input_type] || "text";


  return (
    <div className="automation-input-field">

      <label
        htmlFor={
          `automation-${input.key}`
        }
      >
        {input.label}

        {input.required
          ? " *"
          : ""}
      </label>

      <input
        id={
          `automation-${input.key}`
        }
        type={htmlType}
        required={input.required}
        autoComplete={
          input.secret
            ? "off"
            : undefined
        }
        value={value ?? ""}
        placeholder={
          input.placeholder || ""
        }
        onChange={(event) =>
          onChange(
            input,
            event
          )
        }
        disabled={disabled}
      />

      <AutomationInputHelp
        input={input}
      />

    </div>
  );
}


function AutomationInputHelp({
  input
}) {
  return (
    <div className="automation-input-help">

      <small>
        {input.description}
      </small>

      <div className="automation-input-tags">

        <span>
          {input.scope
            .toUpperCase()}
        </span>

        {input.secret && (
          <span className="automation-input-secret">
            SECRET
          </span>
        )}

      </div>

    </div>
  );
}

export default App;
