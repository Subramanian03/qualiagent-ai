from backend.ai.provider import (
    AIProvider,
)


class MockAIProvider(AIProvider):

    def generate(
        self,
        system_prompt,
        user_prompt,
        task=None
    ):

        if task == "requirement_analysis":
            return self._requirement_analysis()

        if task == "test_case_generation":
            return self._test_cases(
                user_prompt
            )
        if task == "automation_generation":
            return self._automation_code(
                user_prompt
            )
        if task == "failure_analysis":
            return self._failure_analysis(
                user_prompt
            )

        return {
            "provider": "mock",
            "response": (
                "Mock AI provider is working."
            )
        }


    def _requirement_analysis(self):

        return {
            "requirement_id": "MOCK-REQ",
            "requirement_summary":
                "Mock requirement analysis",
            "clarity_score": 7,
            "testable": True,
            "risk_level": "medium",

            "acceptance_criteria": [
                (
                    "Valid behaviour should "
                    "complete successfully."
                ),
                (
                    "Invalid input should be "
                    "handled correctly."
                )
            ],

            "positive_scenarios": [
                (
                    "Verify the expected flow "
                    "using valid data."
                )
            ],

            "negative_scenarios": [
                (
                    "Verify behaviour using "
                    "invalid data."
                )
            ],

            "boundary_scenarios": [
                (
                    "Verify minimum and maximum "
                    "allowed input."
                )
            ],

            "security_considerations": [
                (
                    "Sensitive information must "
                    "not be exposed."
                )
            ],

            "usability_considerations": [
                (
                    "Validation messages should "
                    "be clear."
                )
            ],

            "ambiguities": [
                (
                    "Failure behaviour is not "
                    "completely defined."
                )
            ],

            "missing_information": [
                (
                    "Supported environments are "
                    "not specified."
                )
            ],

            "recommended_test_types": [
                "functional",
                "negative",
                "boundary"
            ]
        }


    def _test_cases(
        self,
        user_prompt
    ):

        prompt = user_prompt.lower()

        if "checkout" in prompt:
            return self._checkout_test_cases()

        if (
            "cart" in prompt or
            "basket" in prompt
        ):
            return self._cart_test_cases()

        if (
            "login" in prompt or
            "log in" in prompt or
            "sign in" in prompt
        ):
            return self._login_test_cases()

        return self._generic_test_cases()


    def _checkout_test_cases(self):

        return {
            "test_cases": [
                {
                    "title":
                        "Verify successful product checkout",

                    "test_type":
                        "positive",

                    "priority":
                        "high",

                    "preconditions": [
                        (
                            "Customer has products "
                            "in the shopping cart"
                        ),
                        (
                            "Checkout is available"
                        )
                    ],

                    "test_data": [
                        "Valid customer information"
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                "Open the shopping cart",
                            "expected_result":
                                (
                                    "Products selected "
                                    "for checkout are displayed"
                                )
                        },
                        {
                            "step_number": 2,
                            "action":
                                "Proceed to checkout",
                            "expected_result":
                                (
                                    "Checkout information "
                                    "form is displayed"
                                )
                        },
                        {
                            "step_number": 3,
                            "action":
                                (
                                    "Enter valid customer "
                                    "information and continue"
                                ),
                            "expected_result":
                                (
                                    "Valid information is "
                                    "accepted"
                                )
                        },
                        {
                            "step_number": 4,
                            "action":
                                "Complete the checkout",
                            "expected_result":
                                (
                                    "Checkout completes "
                                    "successfully"
                                )
                        }
                    ],

                    "automation_candidate": True
                },
                {
                    "title":
                        (
                            "Verify checkout with "
                            "missing customer information"
                        ),

                    "test_type":
                        "negative",

                    "priority":
                        "high",

                    "preconditions": [
                        (
                            "Customer has products "
                            "in the shopping cart"
                        ),
                        (
                            "Checkout is available"
                        )
                    ],

                    "test_data": [
                        (
                            "Missing mandatory "
                            "customer information"
                        )
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                "Proceed to checkout",
                            "expected_result":
                                (
                                    "Checkout information "
                                    "form is displayed"
                                )
                        },
                        {
                            "step_number": 2,
                            "action":
                                (
                                    "Leave required customer "
                                    "information empty"
                                ),
                            "expected_result":
                                (
                                    "Missing required data "
                                    "remains identifiable"
                                )
                        },
                        {
                            "step_number": 3,
                            "action":
                                "Attempt to continue",
                            "expected_result":
                                (
                                    "Checkout is prevented "
                                    "with a validation message"
                                )
                        }
                    ],

                    "automation_candidate": True
                }
            ]
        }


    def _cart_test_cases(self):

        return {
            "test_cases": [
                {
                    "title":
                        "Verify product can be added to cart",

                    "test_type":
                        "positive",

                    "priority":
                        "high",

                    "preconditions": [
                        "Product is available"
                    ],

                    "test_data": [
                        "Available product"
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                "Select an available product",
                            "expected_result":
                                (
                                    "Product can be selected"
                                )
                        },
                        {
                            "step_number": 2,
                            "action":
                                "Add the product to the cart",
                            "expected_result":
                                (
                                    "Product is added to "
                                    "the shopping cart"
                                )
                        }
                    ],

                    "automation_candidate": True
                },
                {
                    "title":
                        "Verify cart reflects added product",

                    "test_type":
                        "positive",

                    "priority":
                        "medium",

                    "preconditions": [
                        "Product has been added to cart"
                    ],

                    "test_data": [
                        "Added product"
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                "Open the shopping cart",
                            "expected_result":
                                (
                                    "The added product "
                                    "is displayed"
                                )
                        }
                    ],

                    "automation_candidate": True
                }
            ]
        }


    def _login_test_cases(self):

        return {
            "test_cases": [
                {
                    "title":
                        "Verify successful login",

                    "test_type":
                        "positive",

                    "priority":
                        "high",

                    "preconditions": [
                        "User account exists",
                        "Login page is available"
                    ],

                    "test_data": [
                        "Valid email",
                        "Valid password"
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                "Open the login page",
                            "expected_result":
                                (
                                    "Login page is displayed"
                                )
                        },
                        {
                            "step_number": 2,
                            "action":
                                (
                                    "Enter valid email "
                                    "and password"
                                ),
                            "expected_result":
                                (
                                    "Credentials are accepted"
                                )
                        },
                        {
                            "step_number": 3,
                            "action":
                                "Select the login action",
                            "expected_result":
                                (
                                    "User is authenticated "
                                    "successfully"
                                )
                        }
                    ],

                    "automation_candidate": True
                },
                {
                    "title":
                        "Verify login with invalid password",

                    "test_type":
                        "negative",

                    "priority":
                        "high",

                    "preconditions": [
                        "User account exists",
                        "Login page is available"
                    ],

                    "test_data": [
                        "Valid email",
                        "Invalid password"
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                "Open the login page",
                            "expected_result":
                                (
                                    "Login page is displayed"
                                )
                        },
                        {
                            "step_number": 2,
                            "action":
                                (
                                    "Enter valid email "
                                    "and invalid password"
                                ),
                            "expected_result":
                                (
                                    "Credentials are entered"
                                )
                        },
                        {
                            "step_number": 3,
                            "action":
                                "Select the login action",
                            "expected_result":
                                (
                                    "Login is rejected with "
                                    "a clear error"
                                )
                        }
                    ],

                    "automation_candidate": True
                }
            ]
        }


    def _generic_test_cases(self):

        return {
            "test_cases": [
                {
                    "title":
                        (
                            "Verify expected behaviour "
                            "using valid input"
                        ),

                    "test_type":
                        "positive",

                    "priority":
                        "medium",

                    "preconditions": [
                        (
                            "Required application "
                            "state is available"
                        )
                    ],

                    "test_data": [
                        "Valid input"
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                (
                                    "Perform the behaviour "
                                    "described by the requirement"
                                ),
                            "expected_result":
                                (
                                    "Expected behaviour "
                                    "completes successfully"
                                )
                        }
                    ],

                    "automation_candidate": True
                },
                {
                    "title":
                        (
                            "Verify behaviour using "
                            "invalid input"
                        ),

                    "test_type":
                        "negative",

                    "priority":
                        "medium",

                    "preconditions": [
                        (
                            "Required application "
                            "state is available"
                        )
                    ],

                    "test_data": [
                        "Invalid input"
                    ],

                    "steps": [
                        {
                            "step_number": 1,
                            "action":
                                (
                                    "Perform the behaviour "
                                    "using invalid input"
                                ),
                            "expected_result":
                                (
                                    "Invalid input is "
                                    "handled correctly"
                                )
                        }
                    ],

                    "automation_candidate": True
                }
            ]
        }

    def _automation_code(
        self,
        user_prompt
    ):

        prompt = user_prompt.lower()

        if "checkout" in prompt:
            return {
                "code": self._checkout_automation()
            }

        if (
            "login" in prompt or
            "log in" in prompt or
            "sign in" in prompt
        ):
            return {
                "code": self._login_automation()
            }

        if (
            "cart" in prompt or
            "basket" in prompt
        ):
            return {
                "code": self._cart_automation()
            }

        return {
            "code": self._generic_automation()
        }

    def _login_automation(self):

      return """const { test, expect } = require('@playwright/test');

test('Verify successful login', async ({ page }) => {
  const baseUrl = process.env.BASE_URL;
  const username = process.env.TEST_USERNAME;
  const password = process.env.TEST_PASSWORD;

  if (!baseUrl) {
    throw new Error('BASE_URL is required');
  }

  if (!username) {
    throw new Error('TEST_USERNAME is required');
  }

  if (!password) {
    throw new Error('TEST_PASSWORD is required');
  }

  await page.goto(baseUrl);

  await page
    .locator('[data-test="username"]')
    .fill(username);

  await page
    .locator('[data-test="password"]')
    .fill(password);

  await page
    .locator('[data-test="login-button"]')
    .click();

  await expect(
    page.locator('[data-test="inventory-container"]')
  ).toBeVisible();

  await expect(page).toHaveURL(
    /inventory\\.html/
  );
});
"""
    def _cart_automation(self):

        return """const { test, expect } = require('@playwright/test');

test('Verify product cart behaviour', async ({ page }) => {
  await page.goto(process.env.BASE_URL);

  const addButton = page.getByRole(
    'button',
    {
      name: /add to cart/i
    }
  ).first();

  await addButton.click();

  await page.getByTestId('shopping-cart-link').click();

  await expect(
    page.locator('.cart_item').first()
  ).toBeVisible();
});
"""

    def _checkout_automation(self):

        return """const { test, expect } = require('@playwright/test');

test('Verify product checkout', async ({ page }) => {
  await page.goto(process.env.BASE_URL);

  await page.getByText('Checkout').click();

  await page.getByLabel('First Name').fill(
    process.env.TEST_FIRST_NAME
  );

  await page.getByLabel('Last Name').fill(
    process.env.TEST_LAST_NAME
  );

  await page.getByLabel('Postal Code').fill(
    process.env.TEST_POSTAL_CODE
  );

  await page.getByRole('button', {
    name: /continue/i
  }).click();

  await expect(
    page.getByText(/checkout overview/i)
  ).toBeVisible();
});
"""

    def _generic_automation(self):

        return """const { test, expect } = require('@playwright/test');

test('Generated QualiAgent test', async ({ page }) => {
  await page.goto(process.env.BASE_URL);

  await expect(page).toHaveTitle(/.+/);
});
"""

    def _failure_analysis(
        self,
        user_prompt
    ):

        prompt = str(
            user_prompt or ""
        ).lower()


        if (
            "locator" in prompt
            or
            "heading" in prompt
            or
            "selector" in prompt
        ):

            return {
                "classification":
                    "automation_failure",

                "confidence":
                    0.90,

                "summary": (
                    "The execution evidence "
                    "indicates a likely automation "
                    "assertion or locator problem."
                ),

                "evidence": [
                    (
                        "The automated execution "
                        "failed."
                    ),
                    (
                        "The sanitized evidence "
                        "contains locator, selector, "
                        "or heading-related failure "
                        "information."
                    )
                ],

                "likely_cause": (
                    "The automation appears to "
                    "depend on an assertion or "
                    "locator that does not match "
                    "the observed application "
                    "semantics."
                ),

                "recommendation_type":
                    "update_automation",

                "recommended_action": (
                    "Review the failing assertion "
                    "and create a new DRAFT "
                    "automation version if the "
                    "application behaviour itself "
                    "is correct."
                ),

                "suggested_change_applicable":
                    True,

                "suggested_change_rationale": (
                    "A safer assertion should use "
                    "stable application behaviour "
                    "rather than a brittle locator."
                ),

                "current_code_excerpt":
                    None,

                "suggested_code_excerpt":
                    None,

                "full_replacement_code":
                    None
            }


        return {
            "classification":
                "unknown",

            "confidence":
                0.50,

            "summary": (
                "The available sanitized evidence "
                "does not provide enough "
                "information for a reliable "
                "classification."
            ),

            "evidence": [
                (
                    "The execution has a FAILED "
                    "or ERROR status."
                )
            ],

            "likely_cause": (
                "The root cause cannot be "
                "determined confidently from the "
                "available evidence."
            ),

            "recommendation_type":
                "manual_investigation",

            "recommended_action": (
                "Review the execution logs and "
                "available evidence manually "
                "before changing automation or "
                "application code."
            ),

            "suggested_change_applicable":
                False,

            "suggested_change_rationale": (
                "There is insufficient evidence "
                "to recommend an automation "
                "change safely."
            ),

            "current_code_excerpt":
                None,

            "suggested_code_excerpt":
                None,

            "full_replacement_code":
                None
        }