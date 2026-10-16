from role_archetype_engine import ARCHETYPE_REGISTRY, classify_role_archetype
from role_skills_catalog import get_role_taxonomy, DISCIPLINE_FLAGSHIP_ROLES
from ten_project_catalog import TEN_PROJECT_MATRICES

print("--- TESTING ALL 14 DISCIPLINES ---")
for arch_id, arch_meta in ARCHETYPE_REGISTRY.items():
    flagship = DISCIPLINE_FLAGSHIP_ROLES.get(arch_id)
    tax = get_role_taxonomy(flagship)
    proj_matrix = TEN_PROJECT_MATRICES.get(arch_id, [])
    non_tech = tax.get("non_technical_competencies", [])
    exp_b = tax.get("experience_benchmarks", {})
    dims = arch_meta.get("dimensions", {})
    
    print(f"\n[Discipline: {arch_id}] ({arch_meta['name']})")
    print(f"  - Flagship: {flagship}")
    print(f"  - Dimensions ({len(dims)}): {list(dims.keys())}")
    print(f"  - Projects in Matrix: {len(proj_matrix)}")
    print(f"  - Non-Tech Competencies ({len(non_tech)}): {non_tech[:2]}")
    print(f"  - Exp Benchmarks: {list(exp_b.keys())}")
    
    assert len(proj_matrix) == 10, f"Expected 10 projects for {arch_id}, found {len(proj_matrix)}"
    assert len(dims) >= 3, f"Expected >= 3 dimensions for {arch_id}, found {len(dims)}"
    assert len(non_tech) >= 3, f"Expected >= 3 non-tech competencies for {arch_id}, found {len(non_tech)}"
    assert "fresher" in exp_b and "senior" in exp_b, f"Missing experience benchmarks for {arch_id}"

print("\nSUCCESS: All 14 Disciplines have 10 production projects, authentic dimensions, non-tech competencies & benchmarks!")
