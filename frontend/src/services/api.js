const API_BASE_URL = "http://127.0.0.1:8000";

function buildReportingQuery(
  filters = {}
) {
  const params =
    new URLSearchParams();


  const values = {
    release:
      filters.release,

    environment:
      filters.environment,

    cycle_status:
      filters.cycle_status,

    result_status:
      filters.result_status,

    execution_mode:
      filters.execution_mode
  };


  for (
    const [
      key,
      value
    ]
    of Object.entries(values)
  ) {

    if (
      value !== null &&
      value !== undefined &&
      String(value).trim()
    ) {

      params.set(
        key,
        String(value).trim()
      );
    }
  }


  const query =
    params.toString();


  return query
    ? `?${query}`
    : "";
}

export async function getProjects() {
  const response = await fetch(
    `${API_BASE_URL}/api/projects`
  );

  if (!response.ok) {
    throw new Error("Failed to load projects");
  }

  return response.json();
}


export async function getProjectRequirements(projectId) {
  const response = await fetch(
    `${API_BASE_URL}/api/requirements/project/${projectId}`
  );

  if (!response.ok) {
    throw new Error("Failed to load requirements");
  }

  return response.json();
}


export async function getRequirementTestCases(requirementId) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cases/requirement/${requirementId}`
  );

  if (!response.ok) {
    throw new Error("Failed to load test cases");
  }

  return response.json();
}

export async function createProject(project) {
  const response = await fetch(
    `${API_BASE_URL}/api/projects`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(project)
    }
  );

  if (!response.ok) {
    throw new Error("Failed to create project");
  }

  return response.json();
}

export async function createRequirement(
  projectId,
  requirement
) {
  const response = await fetch(
    `${API_BASE_URL}/api/requirements/project/${projectId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requirement)
    }
  );

  if (response.status === 409) {
    throw new Error(
      "Requirement ID already exists in this project"
    );
  }

  if (!response.ok) {
    throw new Error(
      "Failed to create requirement"
    );
  }

  return response.json();
}

export async function analyseRequirement(
  requirement
) {
  const response = await fetch(
    `${API_BASE_URL}/api/requirements/analyse`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/json"
      },
      body: JSON.stringify({
        requirement_id:
          requirement.requirement_id,
        title:
          requirement.title,
        description:
          requirement.description,
        application_type:
          requirement.application_type
      })
    }
  );

  const data =
    await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to analyse requirement"
    );
  }

  return data;
}

export async function generateRequirementTestCases(
  requirementId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cases/requirement/${requirementId}/generate`,
    {
      method: "POST"
    }
  );

  if (response.status === 409) {
    throw new Error(
      "Test cases already exist for this requirement"
    );
  }

  if (response.status === 404) {
    throw new Error(
      "Requirement was not found"
    );
  }

  if (!response.ok) {
    throw new Error(
      "Failed to generate test cases"
    );
  }

  return response.json();
}

export async function updateTestCaseStatus(
  testCaseId,
  reviewStatus
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cases/${testCaseId}/status`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        review_status: reviewStatus
      })
    }
  );

  if (response.status === 404) {
    throw new Error(
      "Test case was not found"
    );
  }

  if (!response.ok) {
    throw new Error(
      "Failed to update test case status"
    );
  }

  return response.json();
}

export async function updateTestCaseExecutionType(
  testCaseId,
  executionType
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cases/${testCaseId}/execution-type`,
    {
      method: "PATCH",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        execution_type:
          executionType
      })
    }
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to update Test Case execution type"
    );
  }


  return data;
}

export async function getTestCaseAutomation(
  testCaseId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/test-case/${testCaseId}`
  );

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(
      "Failed to load automation"
    );
  }

  return response.json();
}

export async function getAutomationHistory(
  testCaseId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/test-case/${testCaseId}/history`
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      "Failed to load automation history"
    );
  }

  return Array.isArray(data)
    ? data
    : [];
}

export async function getReadyTestCaseAutomation(
  testCaseId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/test-case/${testCaseId}/ready`
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      "Failed to load READY automation"
    );
  }

  return data;
}

export async function createExecution(
  automationScriptId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/executions`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        automation_script_id:
          automationScriptId
      })
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to create execution"
    );
  }

  return response.json();
}


export async function runExecution(
  executionId,
  values
) {
  const response = await fetch(
    `${API_BASE_URL}/api/executions/${executionId}/run`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        values
      })
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      `Execution failed (${response.status})`
    );
  }

  return data;
}


export async function getExecution(
  executionId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/executions/${executionId}`
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load Execution"
    );
  }


  return data;
}

export async function getExecutionScreenshot(
  executionId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/executions/${executionId}/evidence/screenshot`
  );

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(
      "Failed to load execution screenshot"
    );
  }

  return response.blob();
}


export async function getExecutionTrace(
  executionId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/executions/${executionId}/evidence/trace`
  );

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(
      "Failed to load Playwright trace"
    );
  }

  return response.blob();
}

export async function getProjectExecutions(
  projectId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/executions/project/${projectId}`
  );

  if (response.status === 404) {
    throw new Error(
      "Project was not found"
    );
  }

  if (!response.ok) {
    throw new Error(
      "Failed to load execution history"
    );
  }

  return response.json();
}

export async function getProjectQualitySummary(
  projectId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/reports/project/${projectId}/summary`
  );

  const data =
    await response.json();

  if (response.status === 404) {
    throw new Error(
      data.detail ||
      "Project was not found"
    );
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to load project quality summary"
    );
  }

  return data;
}

export async function getProjectCycleQualitySummary(
  projectId,
  filters = {}
) {
  const query =
    buildReportingQuery(
      filters
    );


  const response = await fetch(
    `${API_BASE_URL}/api/reports/project/${projectId}/cycle-quality-summary${query}`
  );


  let data;


  try {

    data = await response.json();

  } catch {

    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load Cycle quality summary"
    );
  }


  return data;
}

export async function getProjectCycleTraceability(
  projectId,
  filters = {}
) {
  const query =
    buildReportingQuery(
      filters
    );


  const response = await fetch(
    `${API_BASE_URL}/api/reports/project/${projectId}/cycle-traceability${query}`
  );


  let data;


  try {

    data = await response.json();

  } catch {

    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load Cycle traceability"
    );
  }


  return data;
}

export async function getRequirementCoverage(
  projectId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/reports/project/${projectId}/coverage`
  );

  const data =
    await response.json();

  if (response.status === 404) {
    throw new Error(
      data.detail ||
      "Project was not found"
    );
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to load requirement coverage"
    );
  }

  return data;
}

export async function getRequirementTestScenarios(
  requirementId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-scenarios/requirement/${requirementId}`
  );

  if (response.status === 404) {
    throw new Error(
      "Requirement was not found"
    );
  }

  if (!response.ok) {
    throw new Error(
      "Failed to load test scenarios"
    );
  }

  return response.json();
}

export async function getScenarioTestCases(
  scenarioId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cases/scenario/${scenarioId}`
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (response.status === 404) {
    throw new Error(
      data?.detail ||
      "Test scenario was not found"
    );
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      `Failed to load scenario test cases (${response.status})`
    );
  }

  return data;
}

export async function createTestScenario(
  requirementId,
  scenario
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-scenarios/requirement/${requirementId}`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify(
        scenario
      )
    }
  );

  const data =
    await response.json();

  if (response.status === 404) {
    throw new Error(
      data.detail ||
      "Requirement was not found"
    );
  }

  if (response.status === 409) {
    throw new Error(
      data.detail ||
      "Scenario ID already exists"
    );
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to create test scenario"
    );
  }

  return data;
}

export async function generateRequirementScenarios(
  requirementId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-scenarios/requirement/${requirementId}/generate`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/json"
      }
    }
  );

  const data =
    await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to generate test scenarios"
    );
  }

  return data;
}

export async function generateScenarioTestCases(
  scenarioId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cases/scenario/${scenarioId}/generate`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/json"
      }
    }
  );

  const data =
    await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to generate AI Test Cases"
    );
  }

  return data;
}

export async function getAutomationInputSchema(
  testCaseId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/test-case/${testCaseId}/inputs`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/json"
      }
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      "Failed to prepare automation inputs"
    );
  }

  return data;
}

export async function getExecutionInputSchema(
  testCaseId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/test-case/${testCaseId}/execution-inputs`
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load execution inputs"
    );
  }


  return data;
}

export async function generateRealAutomation(
  testCaseId,
  values
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/test-case/${testCaseId}/generate-real`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        values
      })
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      `Failed to generate automation (${response.status})`
    );
  }

  return data;
}

export async function reviewAutomation(
  automationId,
  status
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/${automationId}/review`,
    {
      method: "PATCH",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        status
      })
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      `Failed to review automation (${response.status})`
    );
  }

  return data;
}

export async function createHumanEditedAutomation(
  automationId,
  code,
  changeSummary
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/${automationId}/edit`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        code,
        change_summary:
          changeSummary
      })
    }
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      `Failed to create edited automation (${response.status})`
    );
  }


  return data;
}

export async function createAIUpdatedAutomation(
  automationId,
  instruction
) {
  const response = await fetch(
    `${API_BASE_URL}/api/automation/${automationId}/ai-update`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        instruction
      })
    }
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      `Failed to update automation with AI (${response.status})`
    );
  }


  return data;
}

/*
 * ================================
 * TEST CYCLES
 * ================================
 */


export async function getProjectCycleReadiness(
  projectId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/projects/${projectId}/cycle-readiness`
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load Cycle readiness"
    );
  }


  return data;
}


export async function getProjectTestCycles(
  projectId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/projects/${projectId}/test-cycles`
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load Test Cycles"
    );
  }


  return Array.isArray(data)
    ? data
    : [];
}


export async function createTestCycle(
  projectId,
  cycleData
) {
  const response = await fetch(
    `${API_BASE_URL}/api/projects/${projectId}/test-cycles`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify(
        cycleData
      )
    }
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    let message =
      "Failed to create Test Cycle";


    if (
      typeof data?.detail ===
      "string"
    ) {
      message = data.detail;
    }


    throw new Error(
      message
    );
  }


  return data;
}


export async function getTestCycle(
  cycleId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cycles/${cycleId}`
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load Test Cycle"
    );
  }


  return data;
}

export async function getTestCycleSummary(
  cycleId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cycles/${cycleId}/summary`
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {
    throw new Error(
      data?.detail ||
      "Failed to load Test Cycle summary"
    );
  }


  return data;
}


export async function updateTestCycleStatus(
  cycleId,
  status
) {
  const response = await fetch(
    `${API_BASE_URL}/api/test-cycles/${cycleId}/status`,
    {
      method: "PATCH",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        status
      })
    }
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {
    throw new Error(
      data?.detail ||
      "Failed to update Test Cycle status"
    );
  }


  return data;
}


export async function updateManualCycleResult(
  cycleItemId,
  resultData
) {
  const response = await fetch(
    `${API_BASE_URL}/api/cycle-test-items/${cycleItemId}/manual-result`,
    {
      method: "PATCH",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify(
        resultData
      )
    }
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {
    let message =
      "Failed to save Manual result";


    if (
      typeof data?.detail ===
      "string"
    ) {
      message = data.detail;
    }


    throw new Error(
      message
    );
  }


  return data;
}


export async function getCycleAutomationInputs(
  cycleItemId
) {
  const response = await fetch(
    `${API_BASE_URL}/api/cycle-test-items/${cycleItemId}/automation-inputs`
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {
    throw new Error(
      data?.detail ||
      "Failed to prepare Cycle automation inputs"
    );
  }


  return data;
}


export async function runCycleAutomation(
  cycleItemId,
  values
) {
  const response = await fetch(
    `${API_BASE_URL}/api/cycle-test-items/${cycleItemId}/run-automation`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({
        values
      })
    }
  );


  let data;


  try {
    data = await response.json();
  } catch {
    data = null;
  }


  if (!response.ok) {
    let message =
      "Failed to run Cycle automation";


    if (
      typeof data?.detail ===
      "string"
    ) {
      message = data.detail;
    }


    throw new Error(
      message
    );
  }


  return data;
}

export async function getProjectReleaseQuality(
  projectId,
  release,
  environment = ""
) {
  const params =
    new URLSearchParams();


  params.set(
    "release",
    release
  );


  if (
    environment &&
    String(
      environment
    ).trim()
  ) {

    params.set(
      "environment",
      String(
        environment
      ).trim()
    );
  }


  const response = await fetch(
    `${API_BASE_URL}/api/reports/project/${projectId}/release-quality?${params.toString()}`
  );


  let data;


  try {

    data = await response.json();

  } catch {

    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      "Failed to load Release Quality"
    );
  }


  return data;
}

export async function downloadProjectReleaseQualityPdf(
  projectId,
  release,
  environment = ""
) {
  const params =
    new URLSearchParams();


  params.set(
    "release",
    String(
      release
    ).trim()
  );


  if (
    environment &&
    String(
      environment
    ).trim()
  ) {
    params.set(
      "environment",
      String(
        environment
      ).trim()
    );
  }


  const response = await fetch(
    `${API_BASE_URL}/api/reports/project/${projectId}/release-quality/pdf?${params.toString()}`
  );


  if (!response.ok) {
    let detail =
      "Failed to download Release Quality PDF";


    try {
      const data =
        await response.json();

      detail =
        data?.detail ||
        detail;

    } catch {
      // Keep default message.
    }


    throw new Error(
      detail
    );
  }


  const blob =
    await response.blob();


  const contentDisposition =
    response.headers.get(
      "Content-Disposition"
    );


  let filename =
    "QualiAgent-Release-Quality.pdf";


  if (contentDisposition) {
    const match =
      contentDisposition.match(
        /filename="?([^"]+)"?/i
      );


    if (
      match &&
      match[1]
    ) {
      filename =
        match[1];
    }
  }


  return {
    blob,
    filename
  };
}

export async function downloadProjectReleaseQualityExcel(
  projectId,
  release,
  environment = ""
) {
  const params =
    new URLSearchParams();


  params.set(
    "release",
    String(
      release
    ).trim()
  );


  if (
    environment &&
    String(
      environment
    ).trim()
  ) {

    params.set(
      "environment",
      String(
        environment
      ).trim()
    );
  }


  const response = await fetch(
    `${API_BASE_URL}/api/reports/project/${projectId}/release-quality/excel?${params.toString()}`
  );


  if (!response.ok) {

    let detail =
      "Failed to download Release Quality Excel report";


    try {

      const data =
        await response.json();


      detail =
        data?.detail ||
        detail;


    } catch {

      // Keep the default message.
    }


    throw new Error(
      detail
    );
  }


  const blob =
    await response.blob();


  const contentDisposition =
    response.headers.get(
      "Content-Disposition"
    );


  let filename =
    "QualiAgent-Release-Quality.xlsx";


  if (contentDisposition) {

    const match =
      contentDisposition.match(
        /filename="?([^";]+)"?/i
      );


    if (
      match &&
      match[1]
    ) {

      filename =
        match[1];
    }
  }


  return {
    blob,
    filename
  };
}