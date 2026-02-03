# -*- coding: utf-8 -*-
"""
Gravity Field Dynamics Definitions

A comprehensive reference for the GFD model terminology.
Each definition has a short summary and a detailed explanation.

Usage:
    from gfd_model_v2.common.gfd_definitions import GFD_DEFINITIONS
    
    # Get all definitions
    for term in GFD_DEFINITIONS:
        print(term["name"], "-", term["summary"])
    
    # Look up a specific term
    field_closure = next(d for d in GFD_DEFINITIONS if d["id"] == "field_closure")
"""

# =============================================================================
# GRAVITY FIELD DYNAMICS DEFINITIONS
# =============================================================================

GFD_DEFINITIONS = [
    # =========================================================================
    # PART I: LOGICAL FOUNDATION
    # =========================================================================
    {
        "id": "premise_p1",
        "name": "Premise P1 (Einstein Field Equations)",
        "category": "Foundation",
        "summary": "Stress-energy constrains spacetime geometry through general relativity.",
        "explanation": (
            "The first premise of Gravity Field Dynamics is standard general relativity: "
            "matter and energy determine the curvature of spacetime through the Einstein "
            "field equations. This is not a hypothesis but established physics, confirmed "
            "by over a century of precision tests from Mercury's perihelion to gravitational "
            "wave detection. The equation G_uv = (8*pi*G/c^4)*T_uv encodes how the stress-energy "
            "tensor T_uv constrains the Einstein tensor G_uv, which describes spacetime geometry. "
            "Every prediction of GFD traces back to this foundational relationship."
        )
    },
    {
        "id": "premise_p2",
        "name": "Premise P2 (Geometric Uniqueness)",
        "category": "Foundation",
        "summary": "At each spacetime point, only one geometry can exist.",
        "explanation": (
            "The second premise applies the law of non-contradiction to geometry: a single "
            "point in spacetime cannot simultaneously have two different clock rates, two "
            "different length scales, or two different curvatures. This is not physics but "
            "logic. When two field configurations meet at a boundary, they must resolve to "
            "one consistent geometric state because the alternative, two geometries at the "
            "same point, is logically impossible. This seemingly simple requirement has "
            "profound consequences for how gravitational coupling must work."
        )
    },
    {
        "id": "field_closure",
        "name": "Field Closure",
        "category": "Foundation",
        "summary": "The resolution of gravitational coupling to a unique, consistent geometric state.",
        "explanation": (
            "Field closure is the necessary consequence of combining P1 and P2. When a "
            "field object with stress-energy meets its gravitational environment, the "
            "coupling must resolve to exactly one consistent geometry. This resolution "
            "process is field closure. It is not new physics or a modification of general "
            "relativity. It is simply a name for what must already happen when matter couples "
            "to gravity. Field closure operates through three stages: READ captures both "
            "configurations losslessly, SETTLE resolves them to consistency, and REGISTER "
            "records the outcome. The result is gravity itself, the geometric gradient that "
            "coupling creates."
        )
    },
    
    # =========================================================================
    # PART II: CORE CONSTANTS
    # =========================================================================
    {
        "id": "k_closure_constant",
        "name": "k = 4 (Field Closure Constant)",
        "category": "Constants",
        "summary": "The minimum number of coupling channels required to enclose 3D space.",
        "explanation": (
            "The Field Closure constant k=4 follows from the simplex theorem: to enclose "
            "a region in d dimensions, you need d+1 points. In three spatial dimensions, "
            "this gives k = 3+1 = 4. This is not a fitted parameter but a geometric necessity. "
            "The number 4 appears throughout physics as a consequence: the tetrahedron has "
            "4 faces and 4 vertices, general relativity has 4 ADM constraints (1 Hamiltonian "
            "plus 3 momentum), the tetrad has 4 legs (1 timelike plus 3 spacelike), and "
            "LIGO detects exactly 2 polarizations because 10 - 2k = 2. Carbon forms 4 bonds "
            "and water makes 4 hydrogen bonds for the same geometric reason."
        )
    },
    {
        "id": "d_spatial_dimensions",
        "name": "d = 3 (Spatial Dimensions)",
        "category": "Constants",
        "summary": "The number of spatial dimensions, derived from k.",
        "explanation": (
            "The number of spatial dimensions d = k - 1 = 3 is derived from the Field "
            "Closure constant. This inverts the usual logic: rather than assuming 3 dimensions "
            "and deriving k=4, GFD treats k=4 as fundamental (from closure requirements) and "
            "d=3 as derived. The distinction matters because it suggests dimensionality is not "
            "an arbitrary property of the universe but a consequence of what is required for "
            "consistent field closure. Three spatial dimensions plus one temporal dimension "
            "gives the 3+1 structure of spacetime."
        )
    },
    {
        "id": "field_envelope",
        "name": "Field Envelope (r_e = 2.82 fm)",
        "category": "Constants",
        "summary": "The spherical boundary of a gravity field at the classical electron radius scale.",
        "explanation": (
            "The Field Envelope is the characteristic size of a gravity field, equal to "
            "the classical electron radius r_e = 2.818 femtometers. This scale emerges from "
            "two independent routes that converge to the same value. The electromagnetic route "
            "finds where the electron's self-energy equals its rest mass energy. The gravitational "
            "topology route derives r_e = k*sqrt(G*m_e/a_0). These routes agree to 0.21% across "
            "31 orders of magnitude, suggesting the Field Envelope is a fundamental scale where "
            "electromagnetic and gravitational descriptions meet. Each gravity field is bounded "
            "by a spherical envelope at this scale."
        )
    },
    {
        "id": "mond_acceleration",
        "name": "a_0 (MOND Acceleration Scale)",
        "category": "Constants",
        "summary": "The characteristic acceleration below which gravitational dynamics change behavior.",
        "explanation": (
            "The MOND acceleration scale a_0 is approximately 1.2 x 10^-10 m/s^2, the threshold "
            "below which gravitational dynamics deviate from Newtonian predictions. In GFD, this "
            "scale emerges from the geometry: a_0 = k^2 * (G*m_e/r_e^2) = 16*G*m_e/r_e^2. It also "
            "connects to cosmology through horizon thermodynamics: a_0 = c*H/(2*pi), where H is "
            "the Hubble parameter. This links the smallest gravitational structures (Field Envelopes) "
            "to the largest (the cosmic horizon), suggesting a deep connection between local "
            "geometry and universal dynamics."
        )
    },
    {
        "id": "isotropic_coupling",
        "name": "k^2 = 16 (Isotropic Coupling Factor)",
        "category": "Constants",
        "summary": "The total number of coupling channels when gravity couples through all directions.",
        "explanation": (
            "When gravity couples isotropically through all tetrad components, it engages "
            "k^2 = 16 coupling channels. This arises from the structure of the Field Chamber: "
            "4 inner configurations times 4 outer faces gives 16 total pathways for field "
            "information flow. The factor appears in the relationship between the MOND "
            "acceleration scale and the Field Envelope geometry. It represents the full "
            "coupling capacity when all constraint directions are active simultaneously."
        )
    },
    
    # =========================================================================
    # PART III: FIELD DYNAMICS
    # =========================================================================
    {
        "id": "net_field",
        "name": "NET Field",
        "category": "Field Dynamics",
        "summary": "The gravitational environment from all external sources at a given location.",
        "explanation": (
            "The NET Field is the combined gravitational configuration from everything "
            "outside a field object, as experienced at that object's location. Think of a "
            "river: much has happened upstream, but what a boat encounters is only the current "
            "here and now. The NET Field is the effective background that any object couples "
            "to. It is always capitalized in text because it names a specific concept: not "
            "a generic field, but the registered output from all larger-scale closures that "
            "defines the local gravitational environment."
        )
    },
    {
        "id": "field_object",
        "name": "Field Object",
        "category": "Field Dynamics",
        "summary": "A unified matter configuration that sources gravity as a correlated whole.",
        "explanation": (
            "A field object is any concentration of stress-energy, whether a planet, star, "
            "galaxy, or atom, that participates in gravitational coupling. The key insight "
            "is that field closure couples to the unified configuration, not to its internal "
            "parts separately. Like a chord on a piano where the relationships between notes "
            "define the sound, a field object's internal correlations matter. You cannot "
            "couple to half a field object any more than you can hear half a chord. This "
            "unity is why the equivalence principle holds: gravity responds to total "
            "stress-energy, blind to internal composition."
        )
    },
    {
        "id": "closure_boundary",
        "name": "Closure Boundary",
        "category": "Field Dynamics",
        "summary": "The geometric locus where field object meets NET Field and coupling resolves.",
        "explanation": (
            "The closure boundary, denoted by the Greek letter Sigma, is the interface where "
            "the field object and NET Field meet. It is not a physical surface but a geometric "
            "locus, the location where the coupling constraint must be satisfied. Neither "
            "field owns the boundary; it is neutral ground where both must achieve consistency. "
            "The closure boundary is an input to the field closure process, chosen for evaluation. "
            "The registered boundary state that emerges is the output. This distinction between "
            "where we evaluate (input) and what results (output) is essential to understanding "
            "field closure."
        )
    },
    {
        "id": "read_fss",
        "name": "READ (Full-State Snapshot)",
        "category": "Field Dynamics",
        "summary": "The lossless capture of both field configurations at the closure boundary.",
        "explanation": (
            "READ is the first stage of field closure, where both the field object and NET "
            "Field configurations are captured at the closure boundary. This capture is "
            "lossless because both configurations exist in the same local geometry. In quantum "
            "field theory on curved spacetime, all fields share the local metric, so there "
            "is no geometric mismatch requiring translation or approximation. Same geometry "
            "means no information is lost in the read. This is testable: if coupling were "
            "lossy, we would observe gravitational wakes, drag, or hysteresis as objects "
            "move through gravitational fields. We observe none of these."
        )
    },
    {
        "id": "settle",
        "name": "SETTLE (Settlement)",
        "category": "Field Dynamics",
        "summary": "The resolution of coupling to a unique, consistent geometric state.",
        "explanation": (
            "SETTLE is the second stage of field closure, where the captured configurations "
            "resolve to consistency. By Premise P2, only one geometry can exist at each point, "
            "so settlement is the achievement of that uniqueness. Settlement is distinct from "
            "processing: settlement describes what happens (resolution to consistency), while "
            "processing describes how it happens (distributed constraint enforcement). The "
            "settlement process is atomic, meaning either all k=4 coupling channels achieve "
            "consistency or no valid state exists. Partial settlement is geometrically "
            "forbidden."
        )
    },
    {
        "id": "field_state_registration",
        "name": "Field State Registration",
        "category": "Field Dynamics",
        "summary": "The recorded outcome of field closure that determines the settled geometry.",
        "explanation": (
            "Field State Registration is the final output of field closure: the boundary "
            "state that satisfies the consistency constraint. Formally written as B*_Sigma, "
            "it encodes the field values and their derivatives at the closure boundary after "
            "settlement completes. Registration is the outcome, what we get, while settlement "
            "is the process, how we get there. The registered state then propagates through "
            "the domain, determining the geometry throughout. This is how coupling creates "
            "gravity: the registered state defines the geometric gradient that objects "
            "experience as gravitational acceleration."
        )
    },
    
    # =========================================================================
    # PART IV: FIELD ARCHITECTURE
    # =========================================================================
    {
        "id": "field_chamber",
        "name": "Field Chamber",
        "category": "Architecture",
        "summary": "The tetrahedral interior volume bounded by four Coupling Ports.",
        "explanation": (
            "The Field Chamber is the interior of a gravity field, bounded by k=4 triangular "
            "faces called Coupling Ports. Its geometry is a regular tetrahedron with 4 faces, "
            "4 vertices, and 6 edges. The characteristic scale is the Field Envelope radius "
            "r_e = 2.82 femtometers. Each Field Chamber represents one unit of gravitational "
            "field structure. The tetrahedral shape is not arbitrary but follows from the "
            "closure requirement: k=4 coupling channels correspond to the 4 faces of the "
            "simplest possible 3D enclosure."
        )
    },
    {
        "id": "coupling_port",
        "name": "Coupling Port",
        "category": "Architecture",
        "summary": "A triangular face of the tetrahedron through which field coupling occurs.",
        "explanation": (
            "A Coupling Port is one of the k=4 triangular faces of the Field Chamber through "
            "which gravitational coupling occurs. Each port is an equilateral triangle with "
            "d=3 vertices, corresponding to the three spatial dimensions. The port provides "
            "one of the four constraint directions required for complete closure. When field "
            "closure operates, information flows through all four Coupling Ports simultaneously, "
            "ensuring the coupling is complete and consistent. The geometry of the port, with "
            "its 4 internal triads, connects to the Principle of Interface Parity."
        )
    },
    {
        "id": "stellated_octahedron",
        "name": "Stellated Octahedron (Dual Field Chamber)",
        "category": "Architecture",
        "summary": "Two interpenetrating tetrahedra forming the complete dual structure of a gravity field.",
        "explanation": (
            "The Stellated Octahedron is the complete geometric structure of a gravity field, "
            "formed by two interpenetrating tetrahedra whose vertices lie at the eight corners "
            "of a cube. It has 2k=8 vertices and 2k=8 faces, with central symmetry and the "
            "property of being self-dual. The two component tetrahedra are called Tetrahedron A "
            "(odd parity vertices) and Tetrahedron B (even parity vertices). This dual structure "
            "is essential: Tetrahedron A corresponds to the physical metric while Tetrahedron B "
            "corresponds to the reference metric. Their intersection at the Field Origin is "
            "where coupling achieves consistency."
        )
    },
    {
        "id": "tetrahedron_a",
        "name": "Tetrahedron A",
        "category": "Architecture",
        "summary": "The odd-parity tetrahedron corresponding to the physical metric.",
        "explanation": (
            "Tetrahedron A is one half of the stellated octahedron, with vertices at positions "
            "where the binary coordinate sum is odd: (0,0,1), (0,1,0), (1,0,0), and (1,1,1). "
            "Its apex is at V_7 = (1,1,1). In the bimetric interpretation, Tetrahedron A "
            "corresponds to the physical metric g_uv, the geometry that matter experiences. "
            "The odd parity of its vertices distinguishes it from Tetrahedron B, and this "
            "distinction is preserved under the symmetry operations of the dual Field Chamber. "
            "Tetrahedron A has 1 TIME face pointing inward and 3 SPATIAL faces pointing outward."
        )
    },
    {
        "id": "tetrahedron_b",
        "name": "Tetrahedron B",
        "category": "Architecture",
        "summary": "The even-parity tetrahedron corresponding to the reference metric and binding location.",
        "explanation": (
            "Tetrahedron B is the complementary half of the stellated octahedron, with vertices "
            "at positions where the binary coordinate sum is even: (0,0,0), (0,1,1), (1,0,1), "
            "and (1,1,0). Its apex is at V_0 = (0,0,0). In the bimetric interpretation, "
            "Tetrahedron B corresponds to the reference metric f_uv. In nuclear binding, "
            "Tetrahedron B is where gravity fields pack when atoms form. The even parity "
            "vertices are bitwise complements of Tetrahedron A vertices, creating the "
            "interlocking structure that enables consistent coupling."
        )
    },
    {
        "id": "field_origin",
        "name": "Field Origin",
        "category": "Architecture",
        "summary": "The geometric center where Tetrahedra A and B meet; the coupling null point.",
        "explanation": (
            "The Field Origin is the geometric center of the stellated octahedron, located "
            "at coordinates (0.5, 0.5, 0.5) in the unit cube. This is where Tetrahedron A "
            "and Tetrahedron B meet, and where all compression vectors cancel to create a "
            "null point. The Field Origin is the coupling point where the symmetric vielbein "
            "condition is satisfied, the only location where ghost-free bimetric interaction "
            "can occur. In the stellar forge process, the Field Origin is the gateway through "
            "which gravity fields must pass to bind into atoms. Only unbound fields can "
            "pass through; atoms with outward compression are blocked."
        )
    },
    {
        "id": "time_face",
        "name": "TIME Face",
        "category": "Architecture",
        "summary": "The inward-pointing face opposite the apex of each tetrahedron, related to spin.",
        "explanation": (
            "Each tetrahedron has one TIME face: the face opposite its apex, pointing inward "
            "toward the Field Origin. With 2 tetrahedra, there are 2 TIME faces total. These "
            "faces are physically significant because they relate to electron spin states. "
            "The two TIME faces correspond to the two possible spin projections (+1/2 and -1/2), "
            "determined by which tetrahedron's TIME face is activated. This connects the "
            "geometric structure of the Field Chamber directly to the quantum mechanical "
            "property of spin. The 2 TIME faces plus 6 SPATIAL faces give the total 2k=8 faces."
        )
    },
    {
        "id": "spatial_face",
        "name": "SPATIAL Face",
        "category": "Architecture",
        "summary": "The outward-pointing faces sharing the apex vertex, related to spatial dimensions.",
        "explanation": (
            "Each tetrahedron has three SPATIAL faces: the faces that share the apex as a "
            "vertex and point outward from the Field Origin. With 2 tetrahedra, there are "
            "6 SPATIAL faces total. These correspond to the d=3 spatial dimensions, with each "
            "tetrahedron contributing one face per dimension. The 3+1 structure of spacetime "
            "is encoded in the face structure: each tetrahedron has 1 TIME face plus 3 SPATIAL "
            "faces, giving the 3+1 = 4 total faces required for closure. This is not coincidence "
            "but geometric necessity."
        )
    },
    {
        "id": "port_ratio",
        "name": "Port Ratio (1/d = 1/3)",
        "category": "Architecture",
        "summary": "The fundamental charge quantum derived from the Coupling Port geometry.",
        "explanation": (
            "The Port Ratio is 1/d = 1/3, the conversion factor between continuous Field "
            "Envelope geometry and discrete Field Chamber structure. This ratio also gives "
            "the minimum electric charge quantum: quark charges are integer multiples of 1/3 "
            "(up quark = +2/3, down quark = -1/3). In GFD, quark charges emerge from vertex "
            "activation patterns on the Coupling Port. The up quark's +2/3 charge corresponds "
            "to 2 active vertices, the down quark's -1/3 to 1 active vertex on Tetrahedron B. "
            "This connects charge quantization to the geometry of the Field Chamber."
        )
    },
    
    # =========================================================================
    # PART V: PRINCIPLES AND LAWS
    # =========================================================================
    {
        "id": "interface_parity",
        "name": "Principle of Interface Parity",
        "category": "Principles",
        "summary": "Coherent coupling requires the face subdivision count to equal the closure constant.",
        "explanation": (
            "The Principle of Interface Parity states that coherency in field coupling is "
            "maintained when the internal subdivision count s equals the topological closure "
            "constant k. In a k=4 system, each Coupling Port face has 4 internal triads, and "
            "a 4-state face-read ensures each triad is phase-locked with its neighbors. This "
            "converts linear gravimetric flux into coherent angular momentum without entropy "
            "loss. When s < k, some closure channels are unmatched, causing field leakage. "
            "When s > k, redundant subdivisions create destructive interference. Only when "
            "s = k does perfect parity ensure every triad maps to exactly one channel, "
            "producing the coherent rotation that manifests as the electric field."
        )
    },
    {
        "id": "interpolating_function",
        "name": "Interpolating Function mu(x)",
        "category": "Principles",
        "summary": "The function relating Newtonian and effective gravitational accelerations.",
        "explanation": (
            "The interpolating function mu(x) = x/(1+x) emerges from geometric constraints "
            "on field closure, where x = |grad(Phi)|/a_0 is the ratio of local gravitational "
            "acceleration to the MOND scale. In the Newtonian regime (x >> 1), mu approaches 1 "
            "and standard gravity applies. In the deep-MOND regime (x << 1), mu approaches x "
            "and dynamics change. The function has a beautiful reciprocal symmetry: "
            "mu(x) + mu(1/x) = 1. This is not fitted to data but derived from how field "
            "closure channels fill as gravitational acceleration varies. The transition "
            "at x = 1 (where mu = 0.5) defines the processing boundary."
        )
    },
    {
        "id": "processing_boundary",
        "name": "Processing Boundary (r_c)",
        "category": "Principles",
        "summary": "The radius where gravitational acceleration equals the MOND scale.",
        "explanation": (
            "The processing boundary r_c = sqrt(G*M/a_0) is the radial distance where the "
            "dimensionless gradient intensity x = 1, marking the transition between Newtonian "
            "and deep-MOND regimes. Inside r_c, field closure operates approximately in the "
            "Newtonian mode with mu near 1. Outside r_c, closure transitions to the "
            "low-acceleration regime where mu approaches x. For the Sun, r_c is about 7000 AU, "
            "far beyond the planets but within the Oort cloud. For galaxies, r_c typically "
            "lies within the visible disk, which is why galactic rotation curves show the "
            "flat profiles characteristic of the MOND regime."
        )
    },
    {
        "id": "closure_locality",
        "name": "Closure Locality Principle",
        "category": "Principles",
        "summary": "Tetrahedral closure is local to one Tetrahedron B; partial closures cannot combine.",
        "explanation": (
            "The Closure Locality Principle states that k=4 closure must occur within a "
            "single Tetrahedron B. You cannot combine partial closures across different "
            "structures to achieve stability. The simplex theorem requires d+1 = 4 points "
            "in the same structure to enclose 3D space. Four points distributed as 2+2 across "
            "two separate tetrahedra form two disconnected line segments, not an enclosed "
            "volume. This is why two hydrogen atoms (each k=1 in their own Tet B) do not "
            "spontaneously become helium, and why Beryllium-8 (k=8 = 2x4) is unstable: "
            "two complete tetrahedra cannot nest into one stable configuration."
        )
    },
    
    # =========================================================================
    # PART VI: STELLAR FORGE TERMINOLOGY
    # =========================================================================
    {
        "id": "gravity_field_unit",
        "name": "Gravity Field (Unit)",
        "category": "Stellar Forge",
        "summary": "A single MOND-spherical cell with tetrahedral closure geometry at scale r_e.",
        "explanation": (
            "A gravity field is the fundamental unit of gravitational field structure: a "
            "MOND-spherical cell at the Field Envelope scale r_e = 2.82 femtometers with "
            "k=4 tetrahedral closure geometry. Each gravity field contains a Field Chamber "
            "(the tetrahedral interior), four Coupling Ports (the triangular faces), a Vortex "
            "at its center (the electron pattern), and a Field Origin (the central coupling "
            "point). Gravity fields can be empty (pure spacetime geometry) or activated "
            "(containing nucleon content). The distinction determines whether they can "
            "participate in nuclear binding."
        )
    },
    {
        "id": "empty_gravity_field",
        "name": "Empty Gravity Field",
        "category": "Stellar Forge",
        "summary": "Spacetime substrate with no particle content; the medium through which atoms move.",
        "explanation": (
            "An empty gravity field is pure spacetime geometry with no particle content. "
            "Its Tetrahedron B is unoccupied, compression flows inward toward the center, "
            "and it cannot participate in nuclear binding. Empty fields provide the medium "
            "for spatial translation: atoms move through space by continuously coupling and "
            "decoupling with empty gravity fields. Two empty fields cannot bind because there "
            "is nothing to pack, just coexisting geometry. Empty fields cannot bind electrons "
            "because there is no central charge to attract the vortex. This explains why the "
            "vacuum is stable: spacetime geometry alone does not self-collapse."
        )
    },
    {
        "id": "activated_gravity_field",
        "name": "Activated Gravity Field",
        "category": "Stellar Forge",
        "summary": "A nucleon (proton or neutron) with internal structure that can participate in binding.",
        "explanation": (
            "An activated gravity field is a gravity field with particle content, specifically "
            "a nucleon (proton or neutron). It is created when approximately 938 MeV of energy "
            "excites an empty gravity field into a proton configuration. Activated fields "
            "contribute to the mass number A, with each nucleon adding 1 to A. They can "
            "participate in nuclear binding by packing into Tetrahedron B of a host field. "
            "Protons can bind electrons because they have a central charge that attracts the "
            "vortex pattern. The distinction between empty and activated fields is fundamental: "
            "empty fields are the stage, activated fields are the actors."
        )
    },
    {
        "id": "vortex",
        "name": "Vortex",
        "category": "Stellar Forge",
        "summary": "A stable circulating field pattern; the electron IS this vortex.",
        "explanation": (
            "A vortex is a stable circulating pattern in the field structure, analogous to "
            "a hurricane with an eye at its center. Outside the eye, the field flows inward; "
            "inside, the pattern inverts. This reversal creates stability. The key insight "
            "is that the electron is not a particle orbiting the nucleus in the classical "
            "sense; the electron IS the vortex pattern itself. The electric field emerges "
            "from vortex dynamics when gravity fields compress through each other's Field "
            "Origins. The vortex explains electron behavior without requiring a point particle."
        )
    },
    {
        "id": "vortex_eye",
        "name": "Vortex Eye (Field Origin Gateway)",
        "category": "Stellar Forge",
        "summary": "The center of the vortex where the radial gradient reverses; the gateway to binding.",
        "explanation": (
            "The Vortex Eye is the center of the vortex pattern where the radial gradient "
            "reverses direction. It coincides with the Field Origin at the geometric center "
            "of the gravity field. The Vortex Eye serves as the gateway to element formation: "
            "when stellar compression forces a gravity field through another's vortex eye, "
            "the entering field packs into Tetrahedron B, and binding occurs. This is the "
            "physical process underlying nuclear fusion. Only unbound fields (squish balls) "
            "can pass through; atoms with outward compression (bowling balls) are blocked "
            "by the compression barrier."
        )
    },
    {
        "id": "gravity_knot",
        "name": "Gravity Knot",
        "category": "Stellar Forge",
        "summary": "A coupled gravity field configuration; atoms ARE gravity knots.",
        "explanation": (
            "A gravity knot is a coupled configuration formed when one or more gravity fields "
            "enter through another's Field Origin and pack into Tetrahedron B. This binding "
            "creates atoms: atoms ARE gravity knots. Like a knot in a rope, the configuration "
            "cannot be smoothly untied without extreme energy input. The binding requires "
            "fields to be unbound first (squish ball state), then pass through the Field "
            "Origin, pack into Tet B, trigger the bidirectional compression shift, and form "
            "a stable configuration (bowling ball state). The spherical packing geometry "
            "within Tetrahedron B determines atomic stability."
        )
    },
    {
        "id": "bidirectional_compression_shift",
        "name": "Bidirectional Compression Shift",
        "category": "Stellar Forge",
        "summary": "The reversal of compression direction when gravity fields bind, releasing energy.",
        "explanation": (
            "The bidirectional compression shift is the reversal of field compression direction "
            "that occurs when gravity fields bind. In an empty field, compression flows inward "
            "toward Tetrahedron B with the TIME face at the Tet B apex active. When fields "
            "pack into Tet B, this space becomes occupied and compression reverses to flow "
            "outward, switching the active TIME face to the Tet A apex. This shift releases "
            "binding energy. For helium-4 formation (four fields packing into one Tet B), "
            "the shift releases 26.7 MeV, accounting for the 0.7% mass defect. This energy "
            "release is the source of stellar power."
        )
    },
    {
        "id": "compression_blocking",
        "name": "Compression Blocking Mechanism",
        "category": "Stellar Forge",
        "summary": "Atoms cannot pass through field origins because outward compression blocks entry.",
        "explanation": (
            "The compression blocking mechanism explains why atoms cannot simply merge: their "
            "outward compression (from the bidirectional shift) blocks entry through other "
            "field origins. Think of a bowling ball versus a squish ball. A hydrogen atom "
            "(1+1 configuration) has outward compression, making it rigid and pressurized "
            "like a bowling ball that cannot be squeezed through a small opening. An unbound "
            "gravity field has no compression, soft and empty like a squish ball that passes "
            "through easily. To fuse atoms, stellar energy must overcome the outward compression, "
            "unbinding the atoms into squish balls before they can re-bind. This is the "
            "Coulomb barrier in geometric terms."
        )
    },
    {
        "id": "uniform_spin",
        "name": "Uniform Spin (Chirality)",
        "category": "Stellar Forge",
        "summary": "All gravity fields share the same spin direction; required for consistent coupling.",
        "explanation": (
            "Uniform spin means all gravity fields in the universe share the same chirality "
            "or spin direction. This is geometrically required because only same-spin fields "
            "can couple; opposite-spin fields would annihilate. When same-spin fields meet, "
            "their complementary faces (FACE_A7 and FACE_B0) interlock like a lock and key, "
            "enabling coupling. When opposite-spin fields meet, identical faces collide, "
            "causing destructive interference and annihilation, like matter meeting antimatter. "
            "This uniform chirality enables spatial translation: atoms can move through space "
            "because every empty field presents the correct complementary face."
        )
    },
    {
        "id": "spatial_translation",
        "name": "Spatial Translation",
        "category": "Stellar Forge",
        "summary": "How atoms move by continuously coupling and decoupling with empty gravity fields.",
        "explanation": (
            "Spatial translation is the mechanism by which atoms move through space. An atom "
            "continuously couples with one empty gravity field, decouples, and couples with "
            "the next. This works because uniform spin ensures every empty field presents "
            "the correct complementary face. At position N, the atom's FACE_A7 interlocks "
            "with field N's FACE_B0. As the atom moves, it decouples from N and couples with "
            "N+1, which also presents FACE_B0 due to uniform spin. The process repeats "
            "indefinitely. It is like a train on tracks: the wheels always fit the rails "
            "because the geometry is universal."
        )
    },
    {
        "id": "k_multiple_stability",
        "name": "k-Multiple Stability",
        "category": "Stellar Forge",
        "summary": "Stable nuclear configurations have mass numbers that are multiples of k=4.",
        "explanation": (
            "Stable nuclear configurations follow k-multiples because only complete tetrahedral "
            "closures are geometrically stable. The mass number A equals the number of activated "
            "gravity fields packed into Tetrahedron B. Hydrogen (A=1) has k=1 in Tet B, giving "
            "point geometry with no 3D closure but still triggering the bidirectional shift. "
            "Helium-4 (A=4) achieves the first complete k=4 closure with full 3D enclosure. "
            "Carbon-12 (A=12=3k) has three nested tetrahedra. Iron-56 (A=56=14k) represents "
            "maximum binding efficiency. Configurations like A=2 (line) or A=8 (two separate "
            "tetrahedra) are unstable because they lack proper closure geometry."
        )
    },
    {
        "id": "electron_embedding",
        "name": "Electron Embedding",
        "category": "Stellar Forge",
        "summary": "When extreme compression forces the electron vortex through the Field Origin.",
        "explanation": (
            "Electron embedding occurs when an electron vortex is compressed through a gravity "
            "field's Field Origin into the interior. Under normal conditions, the electron "
            "vortex orbits outside the Field Origin. But at extreme densities (around 10^11 "
            "kg/m^3), the orbit shrinks to the Field Envelope scale. At threshold, the vortex "
            "passes through the eye, and the gravity field folds around it. The result is a "
            "neutron: a gravity field with internal structure from the embedded electron. "
            "This is the geometric interpretation of electron capture. A neutrino carries "
            "away excess energy and lepton number."
        )
    },
    {
        "id": "stellar_compression",
        "name": "Stellar Compression",
        "category": "Stellar Forge",
        "summary": "The stellar process that forces gravity fields through Field Origins to create elements.",
        "explanation": (
            "Stellar compression is the process by which stars create elements. The stellar "
            "core provides the sustained pressure and temperature needed to overcome the "
            "compression blocking barrier. The process begins with gas cloud collapse when "
            "mass exceeds the Jeans limit. Core temperature rises as gravity fields approach "
            "each other. At ignition, the fusion rate exceeds cooling, becoming self-sustaining. "
            "In the stable furnace phase, radiation pressure balances gravity. Throughout, "
            "stellar energy unbinds atoms (bowling balls to squish balls), allowing them to "
            "pass through Field Origins and pack into Tetrahedron B, forming heavier elements. "
            "Each generation of stars builds on products of the previous."
        )
    },
    
    # =========================================================================
    # PART VII: FRAME CORRECTIONS
    # =========================================================================
    {
        "id": "frame_correction",
        "name": "Frame Correction sqrt(k/pi)",
        "category": "Constants",
        "summary": "The ratio converting between flat tetrahedral topology and curved spherical boundary.",
        "explanation": (
            "The frame correction factor sqrt(k/pi) = sqrt(4/pi) = 1.128 converts between "
            "the flat tetrahedral topology of the Field Chamber (characterized by k=4) and "
            "the curved spherical boundary of the Field Envelope (characterized by pi). "
            "When making measurements, the flat and curved descriptions give slightly different "
            "values, and this factor reconciles them. The Hubble parameter, for example, has "
            "the relationship H_measured = H_flat / sqrt(k/pi). This correction appears whenever "
            "comparing tetrahedral (discrete, flat) and spherical (continuous, curved) "
            "descriptions of the same underlying geometry."
        )
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_definition(term_id):
    """Get a definition by its ID."""
    for d in GFD_DEFINITIONS:
        if d["id"] == term_id:
            return d
    return None


def get_definitions_by_category(category):
    """Get all definitions in a category."""
    return [d for d in GFD_DEFINITIONS if d["category"] == category]


def get_all_categories():
    """Get list of all unique categories."""
    return list(set(d["category"] for d in GFD_DEFINITIONS))


def search_definitions(query):
    """Search definitions by name or summary."""
    query = query.lower()
    results = []
    for d in GFD_DEFINITIONS:
        if query in d["name"].lower() or query in d["summary"].lower():
            results.append(d)
    return results


# =============================================================================
# QUICK REFERENCE
# =============================================================================

def print_quick_reference():
    """Print a quick reference of all terms."""
    categories = get_all_categories()
    for cat in sorted(categories):
        print(f"\n=== {cat} ===")
        for d in get_definitions_by_category(cat):
            print(f"  {d['name']}: {d['summary']}")


if __name__ == "__main__":
    print("Gravity Field Dynamics Definitions")
    print("=" * 50)
    print(f"Total definitions: {len(GFD_DEFINITIONS)}")
    print_quick_reference()
