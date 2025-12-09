# Design: add-dynamic-list-fields

## Architecture Overview

This feature introduces structured storage for test case items (preconditions, steps, expected results) and a reusable UI component for dynamic list input.

## Database Design

### Option A: Separate Tables (Recommended)
More explicit, easier to query specific item types.

```sql
CREATE TABLE testcase_preconditions (
    id SERIAL PRIMARY KEY,
    testcase_id INTEGER NOT NULL REFERENCES testcases(id) ON DELETE CASCADE,
    order_index INTEGER NOT NULL DEFAULT 0,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE testcase_steps (
    id SERIAL PRIMARY KEY,
    testcase_id INTEGER NOT NULL REFERENCES testcases(id) ON DELETE CASCADE,
    order_index INTEGER NOT NULL DEFAULT 0,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE testcase_expected_results (
    id SERIAL PRIMARY KEY,
    testcase_id INTEGER NOT NULL REFERENCES testcases(id) ON DELETE CASCADE,
    order_index INTEGER NOT NULL DEFAULT 0,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_preconditions_testcase ON testcase_preconditions(testcase_id, order_index);
CREATE INDEX idx_steps_testcase ON testcase_steps(testcase_id, order_index);
CREATE INDEX idx_expected_results_testcase ON testcase_expected_results(testcase_id, order_index);
```

### Option B: Polymorphic Table
Single table with item_type discriminator. Simpler migration, slightly more complex queries.

```sql
CREATE TABLE testcase_items (
    id SERIAL PRIMARY KEY,
    testcase_id INTEGER NOT NULL REFERENCES testcases(id) ON DELETE CASCADE,
    item_type VARCHAR(20) NOT NULL, -- 'precondition', 'step', 'expected_result'
    order_index INTEGER NOT NULL DEFAULT 0,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_items_testcase_type ON testcase_items(testcase_id, item_type, order_index);
```

**Recommendation**: Option A (separate tables) for clarity and simpler SQLAlchemy relationships.

## SQLAlchemy Models

### New Item Models

```python
class TestCasePrecondition(Base):
    __tablename__ = "testcase_preconditions"

    id: Mapped[int] = mapped_column(primary_key=True)
    testcase_id: Mapped[int] = mapped_column(ForeignKey("testcases.id", ondelete="CASCADE"))
    order_index: Mapped[int] = mapped_column(default=0)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    testcase: Mapped["TestCase"] = relationship(back_populates="precondition_items")

class TestCaseStep(Base):
    __tablename__ = "testcase_steps"

    id: Mapped[int] = mapped_column(primary_key=True)
    testcase_id: Mapped[int] = mapped_column(ForeignKey("testcases.id", ondelete="CASCADE"))
    order_index: Mapped[int] = mapped_column(default=0)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    testcase: Mapped["TestCase"] = relationship(back_populates="step_items")

class TestCaseExpectedResult(Base):
    __tablename__ = "testcase_expected_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    testcase_id: Mapped[int] = mapped_column(ForeignKey("testcases.id", ondelete="CASCADE"))
    order_index: Mapped[int] = mapped_column(default=0)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    testcase: Mapped["TestCase"] = relationship(back_populates="expected_result_items")
```

### Updated TestCase Model

```python
class TestCase(Base):
    # ... existing fields ...

    # Deprecated fields (keep temporarily for migration)
    preconditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    steps: Mapped[str] = mapped_column(Text, nullable=False)
    expected_results: Mapped[str] = mapped_column(Text, nullable=False)

    # New relationships
    precondition_items: Mapped[list["TestCasePrecondition"]] = relationship(
        back_populates="testcase",
        cascade="all, delete-orphan",
        order_by="TestCasePrecondition.order_index"
    )
    step_items: Mapped[list["TestCaseStep"]] = relationship(
        back_populates="testcase",
        cascade="all, delete-orphan",
        order_by="TestCaseStep.order_index"
    )
    expected_result_items: Mapped[list["TestCaseExpectedResult"]] = relationship(
        back_populates="testcase",
        cascade="all, delete-orphan",
        order_by="TestCaseExpectedResult.order_index"
    )
```

## Pydantic Schemas

```python
class TestCaseCreate(BaseModel):
    title: str
    description: str | None = None
    preconditions: list[str] = []  # Changed from str | None
    steps: list[str]               # Changed from str, must have at least 1
    expected_results: list[str]    # Changed from str, must have at least 1
    status: TestCaseStatus = TestCaseStatus.DRAFT
    priority: TestCasePriority = TestCasePriority.MEDIUM

    @validator('steps')
    def steps_not_empty(cls, v):
        if not v or all(s.strip() == '' for s in v):
            raise ValueError('At least one step is required')
        return [s for s in v if s.strip()]

    @validator('expected_results')
    def expected_results_not_empty(cls, v):
        if not v or all(s.strip() == '' for s in v):
            raise ValueError('At least one expected result is required')
        return [s for s in v if s.strip()]

class TestCaseResponse(BaseModel):
    id: int
    title: str
    description: str | None
    preconditions: list[str]      # List of items
    steps: list[str]              # List of items
    expected_results: list[str]   # List of items
    # ... other fields
```

## UI Component: DynamicListField

### Structure

```
DynamicListField
├── Header Row
│   ├── Label
│   └── Add Button (+)
├── Items Container (id for JS targeting)
│   └── Item Row × N
│       ├── Input field
│       └── Remove Button (×)
└── Hidden template row (for cloning)
```

### HTML Output

```html
<div class="dynamic-list-field" data-field-name="steps" data-required="true">
    <div class="dynamic-list-header">
        <label class="form-label">Steps <span class="required">*</span></label>
        <button type="button" class="btn-add-item" onclick="addListItem('steps')">
            + Add New
        </button>
    </div>
    <div class="dynamic-list-items" id="steps-items">
        <!-- Items rendered here -->
        <div class="dynamic-list-item" data-index="0">
            <span class="item-number">1.</span>
            <input type="text" name="steps" value="..." class="form-input">
            <button type="button" class="btn-remove-item" onclick="removeListItem(this)">×</button>
        </div>
    </div>
</div>
```

### JavaScript Functions

```javascript
function addListItem(fieldName) {
    const container = document.getElementById(fieldName + '-items');
    const items = container.querySelectorAll('.dynamic-list-item');
    const newIndex = items.length;

    const newItem = document.createElement('div');
    newItem.className = 'dynamic-list-item';
    newItem.dataset.index = newIndex;
    newItem.innerHTML = `
        <span class="item-number">${newIndex + 1}.</span>
        <input type="text" name="${fieldName}" class="form-input" placeholder="Enter item...">
        <button type="button" class="btn-remove-item" onclick="removeListItem(this)">×</button>
    `;
    container.appendChild(newItem);
    newItem.querySelector('input').focus();
}

function removeListItem(button) {
    const item = button.closest('.dynamic-list-item');
    const container = item.parentElement;
    item.remove();
    renumberItems(container);
}

function renumberItems(container) {
    const items = container.querySelectorAll('.dynamic-list-item');
    items.forEach((item, index) => {
        item.dataset.index = index;
        item.querySelector('.item-number').textContent = (index + 1) + '.';
    });
}
```

## Data Migration

### Migration Script Logic

```python
async def migrate_testcase_items():
    """Migrate existing text fields to new item tables."""
    async with get_session() as session:
        testcases = await session.execute(select(TestCase))

        for tc in testcases.scalars():
            # Migrate preconditions
            if tc.preconditions:
                for idx, line in enumerate(tc.preconditions.split('\n')):
                    if line.strip():
                        session.add(TestCasePrecondition(
                            testcase_id=tc.id,
                            order_index=idx,
                            content=line.strip()
                        ))

            # Migrate steps
            for idx, line in enumerate(tc.steps.split('\n')):
                if line.strip():
                    session.add(TestCaseStep(
                        testcase_id=tc.id,
                        order_index=idx,
                        content=line.strip()
                    ))

            # Migrate expected_results
            for idx, line in enumerate(tc.expected_results.split('\n')):
                if line.strip():
                    session.add(TestCaseExpectedResult(
                        testcase_id=tc.id,
                        order_index=idx,
                        content=line.strip()
                    ))

        await session.commit()
```

## Form Submission Flow

1. User clicks "+" to add items, fills in content
2. Form submits with multiple inputs having same name:
   ```
   steps=Step 1 content
   steps=Step 2 content
   steps=Step 3 content
   ```
3. FastAPI receives as `list[str]`
4. Route handler creates item records with order preserved
5. Response returns structured list

## View Page Updates

Display items as ordered lists instead of preformatted text:

```python
# Before
Pre(testcase["steps"], cls="code-block")

# After
Ol(
    *[Li(step) for step in testcase["steps"]],
    cls="testcase-steps-list"
)
```

## CSS Styles

```css
.dynamic-list-field { }
.dynamic-list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.btn-add-item {
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    cursor: pointer;
}
.dynamic-list-items { }
.dynamic-list-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}
.item-number {
    min-width: 2rem;
    color: var(--text-muted);
}
.btn-remove-item {
    background: var(--danger-color);
    color: white;
    border: none;
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
    cursor: pointer;
}
```
