# -*- coding: utf-8 -*-
"""
Gravity Field Dynamics Concepts

A mechanical reference explaining HOW things work in the GFD model.
Unlike definitions (which state WHAT things are), concepts explain
the working principles and physical mechanisms.

Usage:
    from gfd_model_v2.reference.gfd_concepts import GFD_CONCEPTS
    
    for concept in GFD_CONCEPTS:
        print(concept["title"])
        print(concept["content"])
"""

# =============================================================================
# GRAVITY FIELD DYNAMICS CONCEPTS
# =============================================================================

GFD_CONCEPTS = [
    # =========================================================================
    # SECTION I: THE FIELD CHAMBER
    # =========================================================================
    {
        "id": "field_chamber_mechanics",
        "title": "The Field Chamber: Basic Unit of Gravitational Structure",
        "category": "Field Architecture",
        "summary": "How the tetrahedral chamber creates the minimum enclosure for gravitational coupling.",
        "content": (
            "The fundamental unit of gravitational structure is the Field Chamber, a regular "
            "tetrahedron defined by the k=4 topological closure constant. To enclose a region "
            "of three-dimensional space, you need at minimum four points forming four faces. "
            "This is not a design choice but a geometric necessity: fewer than four faces "
            "cannot bound a volume.\n\n"
            "The Field Chamber consists of four triangular Coupling Ports: three spatial faces "
            "that point outward from the center, and one temporal base face that points inward. "
            "This 3+1 structure mirrors the dimensionality of spacetime itself. The three "
            "spatial faces correspond to the three spatial dimensions; the one temporal face "
            "corresponds to the time dimension. When gravitational coupling occurs, information "
            "flows through all four ports simultaneously, ensuring the coupling is complete and "
            "geometrically consistent.\n\n"
            "The characteristic scale of the Field Chamber is the Field Envelope radius "
            "r_e = 2.82 femtometers. This scale emerges from two independent routes: the "
            "electromagnetic self-energy calculation and the gravitational topology derivation. "
            "Their convergence to the same value across 31 orders of magnitude suggests this "
            "is not coincidence but a fundamental scale where electromagnetic and gravitational "
            "descriptions meet."
        )
    },
    {
        "id": "coupling_port_mechanics",
        "title": "Coupling Ports: The Interface for Field Information Flow",
        "category": "Field Architecture",
        "summary": "How triangular faces enable consistent coupling between adjacent fields.",
        "content": (
            "Each face of the Field Chamber functions as a Coupling Port, the interface through "
            "which gravitational information flows between adjacent fields. The port is an "
            "equilateral triangle with three vertices, corresponding to the three spatial "
            "dimensions (d=3). When Field Chambers pack together in the gravitational lattice, "
            "their faces press against the faces of their neighbors, creating direct coupling "
            "channels.\n\n"
            "To maintain fluidic continuity across the lattice, each Coupling Port is subdivided "
            "into four congruent sub-triangles called triads. These four triads act as physical "
            "alignment pins, creating a 1:1 mapping between the internal subdivision count (s=4) "
            "and the global closure constant (k=4). This equality is not arbitrary: it is the "
            "condition required for coherent coupling.\n\n"
            "When the NET Field enters through a Coupling Port, the four triads distribute the "
            "incoming flux to exactly four channels. This perfect distribution ensures no "
            "entropy loss during coupling. If there were fewer triads than channels (s < k), "
            "some channels would be unmatched, causing field leakage. If there were more triads "
            "than channels (s > k), redundant subdivisions would create phase conflicts and "
            "destructive interference. Only when s = k does every triad map to exactly one "
            "channel, producing coherent coupling without geometric mismatch or boundary shearing."
        )
    },
    {
        "id": "triad_mechanics",
        "title": "Triads: Phase-Locking the Gravitational Flux",
        "category": "Field Architecture",
        "summary": "How the four triads per face convert linear flux to angular momentum.",
        "content": (
            "The four triads on each Coupling Port face serve a specific mechanical function: "
            "they phase-lock the incoming gravitational flux with neighboring fields. When the "
            "NET Field arrives at the closure boundary, it carries linear gravimetric flux, a "
            "directional flow of field information. This linear flow must be converted to the "
            "angular structure required for stable field closure.\n\n"
            "The triads accomplish this conversion through geometric constraint. As flux enters "
            "through the central Field Origin, the four triads force it into specific angular "
            "trajectories. Each triad couples to exactly one of the k=4 closure channels, and "
            "because the triads on adjacent faces share vertices, they automatically maintain "
            "phase coherence across the boundary. This is mechanical phase-locking: the geometry "
            "itself enforces the phase relationship.\n\n"
            "The result of this phase-locked coupling is coherent angular momentum within the "
            "Field Chamber. This angular momentum, the vorticity generated by the triad "
            "structure, is not a secondary effect but the specific mechanism that creates the "
            "Electric Field from the gravitational manifold. The triads ensure that the "
            "resulting Vortex remains topologically protected and stable, even under the "
            "high-pressure conditions of spherical packing during element formation."
        )
    },
    
    # =========================================================================
    # SECTION II: THE DUAL STRUCTURE
    # =========================================================================
    {
        "id": "stellated_octahedron_mechanics",
        "title": "The Stellated Octahedron: Dual Structure of a Gravity Field",
        "category": "Dual Architecture",
        "summary": "How two interpenetrating tetrahedra create the complete field structure.",
        "content": (
            "A single tetrahedron provides closure, but complete gravitational field structure "
            "requires a dual configuration: two interpenetrating tetrahedra forming a stellated "
            "octahedron. This compound places vertices at all eight corners of a cube and "
            "creates a structure with 2k=8 vertices and 2k=8 faces. The two component "
            "tetrahedra are distinguished by the parity of their vertex coordinates.\n\n"
            "Tetrahedron A has vertices at positions with odd parity: (0,0,1), (0,1,0), (1,0,0), "
            "and (1,1,1). Tetrahedron B has vertices at positions with even parity: (0,0,0), "
            "(0,1,1), (1,0,1), and (1,1,0). These two sets are bitwise complements of each "
            "other, creating an interlocking structure like two hands with fingers interleaved.\n\n"
            "In the bimetric interpretation, Tetrahedron A corresponds to the physical metric "
            "g_uv (the geometry that matter experiences), while Tetrahedron B corresponds to "
            "the reference metric f_uv (the background against which dynamics are measured). "
            "Stable coupling requires consistency between these two metrics. The stellated "
            "octahedron is the unique geometry that allows both tetrahedra to share a common "
            "center while maintaining their individual closure properties. This dual structure "
            "is why gravity fields can both couple to external fields and maintain internal "
            "consistency."
        )
    },
    {
        "id": "field_origin_mechanics",
        "title": "The Field Origin: Gateway and Null Point",
        "category": "Dual Architecture",
        "summary": "How the geometric center functions as the coupling point and binding gateway.",
        "content": (
            "At the geometric center of the stellated octahedron lies the Field Origin, located "
            "at coordinates (0.5, 0.5, 0.5) in the unit cube. This point has a unique property: "
            "it is where Tetrahedron A and Tetrahedron B meet, and where all compression vectors "
            "from the surrounding structure cancel to zero. The Field Origin is a null point, "
            "the only location where the symmetric vielbein condition is satisfied.\n\n"
            "The Field Origin serves two distinct functions. First, it is the coupling point "
            "where the physical metric and reference metric achieve consistency. Ghost-free "
            "bimetric interaction can only occur where the two metrics align, and the Field "
            "Origin is the unique point satisfying this constraint. Second, it is the gateway "
            "for nuclear binding. When stellar compression forces gravity fields together, they "
            "must pass through the Field Origin of a host field to bind.\n\n"
            "The gateway function is selective. Only unbound gravity fields can pass through "
            "the Field Origin. Bound configurations (atoms) have outward compression from the "
            "bidirectional shift, and this compression blocks entry. The Field Origin thus "
            "acts as a geometric filter: it admits raw fields for binding while rejecting "
            "already-formed structures. This selectivity is the geometric basis of the Coulomb "
            "barrier."
        )
    },
    {
        "id": "time_spatial_face_mechanics",
        "title": "TIME and SPATIAL Faces: The 3+1 Structure",
        "category": "Dual Architecture",
        "summary": "How face orientation encodes spacetime dimensionality and spin states.",
        "content": (
            "Each tetrahedron in the stellated octahedron has four faces, but these faces are "
            "not equivalent. One face, the TIME face, points inward toward the Field Origin; "
            "it is the face opposite the apex vertex. The other three faces, the SPATIAL faces, "
            "share the apex as a vertex and point outward from the center. This gives each "
            "tetrahedron a 1+3 structure: one temporal face plus three spatial faces.\n\n"
            "With two tetrahedra, the complete structure has 2 TIME faces and 6 SPATIAL faces, "
            "totaling 8 faces (2k). The TIME faces are physically significant because they "
            "relate to electron spin. The two possible spin projections (+1/2 and -1/2) "
            "correspond to which tetrahedron's TIME face is activated during field closure. "
            "This is not an analogy but a direct geometric encoding: spin emerges from the "
            "face structure.\n\n"
            "The spin value itself derives from this geometry. The total angular momentum "
            "of the dual structure is L = 2h (one quantum per tetrahedron). The TIME faces "
            "constitute 2 out of 8 total faces, a fraction of 1/4. The observable spin is "
            "this fraction times the total: S = (2/8) x 2h = h/2. This is why electrons "
            "have spin-1/2. The quantum mechanical property follows from the geometric "
            "structure of the Field Chamber."
        )
    },
    
    # =========================================================================
    # SECTION III: FIELD CLOSURE MECHANICS
    # =========================================================================
    {
        "id": "field_closure_process",
        "title": "The Field Closure Process: READ, SETTLE, REGISTER",
        "category": "Closure Mechanics",
        "summary": "How gravitational coupling resolves through three sequential stages.",
        "content": (
            "Field closure is the process by which gravitational coupling achieves consistency. "
            "It operates through three sequential stages: READ, SETTLE, and REGISTER. This "
            "sequence is not a model assumption but a description of what must happen when "
            "two field configurations meet at a boundary.\n\n"
            "READ captures both the field object configuration and the NET Field configuration "
            "at the closure boundary. This capture is lossless because both configurations "
            "exist in the same local geometry. In quantum field theory on curved spacetime, "
            "all fields share the local metric, so there is no geometric mismatch requiring "
            "translation or approximation. If READ were lossy, we would observe gravitational "
            "wakes, drag, or hysteresis. We observe none of these.\n\n"
            "SETTLE resolves the captured configurations to a unique state. By the principle "
            "of geometric uniqueness, only one geometry can exist at each point. SETTLE is "
            "the achievement of that uniqueness, enforcing consistency across all k=4 closure "
            "channels simultaneously. Settlement is atomic: either all channels achieve "
            "consistency or no valid state exists. Partial settlement is geometrically "
            "forbidden.\n\n"
            "REGISTER records the outcome. The registered boundary state B*_Sigma encodes "
            "the field values and their derivatives after settlement. This state then "
            "propagates through the domain, determining the geometry throughout. Gravity "
            "itself, the acceleration that objects experience, is the spatial gradient of "
            "this registered geometry: g = -c^2 grad(l(x))."
        )
    },
    {
        "id": "lossless_coupling_mechanics",
        "title": "Lossless Coupling: Why Field Closure Preserves Information",
        "category": "Closure Mechanics",
        "summary": "How shared geometry enables information-preserving gravitational interaction.",
        "content": (
            "Gravitational coupling is lossless. When a field object couples to the NET Field, "
            "no information is destroyed, no entropy is generated, and no energy is dissipated "
            "in the coupling process itself. This is not an assumption but a consequence of "
            "how coupling works.\n\n"
            "The key is shared geometry. At the closure boundary, both the field object and "
            "the NET Field exist in the same local metric l(x). They share the same clock "
            "rate, the same length scale, and the same curvature. Because they are already "
            "described in the same geometric language, there is no translation required when "
            "READ captures their configurations. Translation is where information loss would "
            "occur; no translation means no loss.\n\n"
            "This losslessness is observable. If coupling were lossy, objects moving through "
            "gravitational fields would experience drag, slowing down over time even in vacuum. "
            "Planets would spiral inward, satellites would decay without atmospheric friction, "
            "and gravitational waves would leave wakes of dissipated energy. None of these "
            "effects are observed. Orbits are stable for billions of years. Gravitational "
            "waves propagate cleanly without trailing disturbances. These observations confirm "
            "that coupling is lossless, exactly as the shared-geometry mechanism requires."
        )
    },
    {
        "id": "closure_locality_mechanics",
        "title": "Closure Locality: Why Partial Closures Cannot Combine",
        "category": "Closure Mechanics",
        "summary": "How the simplex theorem enforces local closure within a single structure.",
        "content": (
            "Tetrahedral closure is a local property. It must occur within a single Tetrahedron B, "
            "not as a sum of partial closures across multiple structures. This constraint, the "
            "Closure Locality Principle, has profound consequences for nuclear stability.\n\n"
            "The geometric reason is the simplex theorem: to enclose d-dimensional space, you "
            "need d+1 points in the same structure. For 3D space, you need 4 points within one "
            "tetrahedron. Four points distributed across two separate tetrahedra (2+2) do not "
            "enclose space; they form two disconnected line segments with no volume between "
            "them. Closure requires all k=4 points together.\n\n"
            "This explains why two hydrogen atoms near each other do not become helium. Each "
            "hydrogen has k=1 closure in its own Tetrahedron B (point geometry). Two separate "
            "point geometries cannot combine into k=4 closure. To make helium-4, you need four "
            "gravity fields packed into one Tetrahedron B, which requires stellar compression "
            "to force all four through a single Field Origin. Proximity alone is not fusion.\n\n"
            "The same principle explains why beryllium-8 is unstable. Two helium-4 nuclei "
            "(each k=4) compressed together give k=8 = 2x4 in one Tetrahedron B. But two "
            "complete tetrahedra cannot nest into a single stable configuration. They "
            "represent two separate closures forced into the same space, creating geometric "
            "frustration. Beryllium-8 decays in 10^-16 seconds, almost instantaneously, "
            "because k=8 cannot form a stable nested closure."
        )
    },
    
    # =========================================================================
    # SECTION IV: THE COMPRESSION SYSTEM
    # =========================================================================
    {
        "id": "compression_direction_mechanics",
        "title": "Compression Direction: Inward vs Outward Flow",
        "category": "Compression System",
        "summary": "How compression direction determines field state and binding capability.",
        "content": (
            "Every gravity field has a compression direction: the direction in which field "
            "pressure flows relative to Tetrahedron B. This direction determines whether "
            "the field can participate in binding and how it interacts with other fields.\n\n"
            "In an empty gravity field (pure spacetime geometry with no particle content), "
            "compression flows inward toward Tetrahedron B. The Tet B interior is unoccupied, "
            "so compression naturally converges toward this empty space. The active TIME face "
            "in this state is FACE_B0, the face at the Tet B apex. This inward-compressing "
            "field is like an empty container, ready to receive content.\n\n"
            "In a bound gravity field (one with content in Tetrahedron B), compression flows "
            "outward. When gravity fields pack into Tet B, that space becomes occupied, and "
            "compression reverses direction to flow away from the filled region. The active "
            "TIME face switches to FACE_A7 at the Tet A apex. This outward-compressing field "
            "is pressurized, pushing against its boundaries.\n\n"
            "The compression direction is not just a descriptor but a functional property. "
            "It determines whether a field can pass through another's Field Origin (inward "
            "compression allows passage; outward compression blocks it) and whether the "
            "field contributes to nuclear stability (outward compression indicates binding "
            "has occurred)."
        )
    },
    {
        "id": "bidirectional_shift_mechanics",
        "title": "The Bidirectional Compression Shift: How Binding Releases Energy",
        "category": "Compression System",
        "summary": "How the reversal of compression direction during binding releases binding energy.",
        "content": (
            "When gravity fields bind, compression direction reverses. This reversal, the "
            "bidirectional compression shift, is the mechanical source of nuclear binding "
            "energy. Understanding this shift explains both why binding is energetically "
            "favorable and where the released energy comes from.\n\n"
            "Before binding, each field has inward compression flowing toward its empty "
            "Tetrahedron B. The system is like a set of springs all pulling inward. When "
            "binding occurs and fields pack into a host's Tet B, that space becomes occupied. "
            "The compression in the bound system cannot continue flowing inward (nowhere to "
            "go), so it reverses to flow outward. The springs now push instead of pull.\n\n"
            "This reversal releases energy. The transition from inward to outward compression "
            "is a change in the field's internal state, and the energy difference appears as "
            "released binding energy. For helium-4 formation (four fields packing into one "
            "Tet B), the bidirectional shift releases 26.7 MeV, accounting for the 0.7% mass "
            "defect between four separate protons and one helium nucleus. This is not energy "
            "appearing from nowhere; it is the energy stored in the inward compression state "
            "being released when that state becomes outward compression."
        )
    },
    {
        "id": "compression_blocking_mechanics",
        "title": "Compression Blocking: The Geometric Coulomb Barrier",
        "category": "Compression System",
        "summary": "How outward compression prevents atoms from merging without stellar energy.",
        "content": (
            "Atoms cannot simply merge because their outward compression blocks entry through "
            "each other's Field Origins. This compression blocking is the geometric mechanism "
            "underlying the Coulomb barrier. Understanding it explains why fusion requires "
            "stellar temperatures even though protons are geometrically smaller than the "
            "Field Origin.\n\n"
            "Think of the analogy: a bowling ball versus a squish ball. A hydrogen atom "
            "(1+1 configuration) has outward compression from the bidirectional shift. It is "
            "rigid and pressurized like a bowling ball. An unbound gravity field has no "
            "compression; it is soft and empty like a squish ball. The bowling ball cannot "
            "be squeezed through a small opening because it actively resists compression. "
            "The squish ball passes through easily because nothing resists.\n\n"
            "When two hydrogen atoms approach, both have outward compression. Their compressions "
            "oppose each other, like two bowling balls pressing together. Neither can enter "
            "the other's Field Origin because each is actively outputting pressure in the "
            "direction of entry. The energy required to overcome this opposition is the Coulomb "
            "barrier, approximately 511 keV at the Field Envelope scale.\n\n"
            "To achieve fusion, stellar energy must unbind the atoms. The process converts "
            "bowling balls back to squish balls by reversing their compression. Only then can "
            "the unbound fields pass through the Field Origin and re-bind as a heavier element. "
            "This is why fusion requires millions of degrees: not to make particles move faster, "
            "but to provide the energy needed to overcome outward compression and enable entry."
        )
    },
    
    # =========================================================================
    # SECTION V: VORTEX MECHANICS
    # =========================================================================
    {
        "id": "vortex_formation_mechanics",
        "title": "Vortex Formation: How Angular Momentum Creates the Electron",
        "category": "Vortex Mechanics",
        "summary": "How coherent angular momentum from triad coupling manifests as the electron.",
        "content": (
            "The electron is not a point particle orbiting a nucleus. The electron IS a vortex "
            "pattern in the field structure, a stable circulation of angular momentum created "
            "by the triad coupling mechanism. This identification resolves long-standing puzzles "
            "about electron behavior.\n\n"
            "Vortex formation begins when linear gravimetric flux enters through the Coupling "
            "Ports. The four triads on each face force this linear flow into angular trajectories, "
            "distributing flux across the k=4 closure channels with perfect phase coherence. The "
            "result is not random circulation but organized vorticity: the field rotates in a "
            "specific pattern determined by the triad geometry.\n\n"
            "This vortex has the structure of a hurricane: outside the eye, field flows inward "
            "in a spiral pattern; at the center (the vortex eye, coinciding with the Field "
            "Origin), the radial gradient reverses. This reversal creates stability. The "
            "pattern cannot unwind because the eye provides a topological anchor.\n\n"
            "The electric field emerges from this vortex dynamics. When we measure electric "
            "charge and electromagnetic interactions, we are measuring the effects of this "
            "coherent angular momentum pattern. The electron's properties (charge, spin, "
            "magnetic moment) all derive from the vortex geometry rather than from an "
            "intrinsic point-like source."
        )
    },
    {
        "id": "electric_field_generation_mechanics",
        "title": "Electric Field Generation: Vorticity as Electromagnetic Source",
        "category": "Vortex Mechanics",
        "summary": "How the vortex pattern within the Field Chamber creates electromagnetic effects.",
        "content": (
            "The Electric Field is not a separate entity from gravity but an emergent property "
            "of the vortex pattern within the Field Chamber. When the triads achieve perfect "
            "Interface Parity (s = k = 4), linear gravimetric flux converts to coherent angular "
            "momentum without entropy loss. This angular momentum, circulating within the "
            "chamber, IS the electromagnetic field.\n\n"
            "The mechanism works through the Principle of Interface Parity. Because the internal "
            "subdivision count (4 triads) equals the topological closure constant (k=4), every "
            "triad maps to exactly one closure channel. This 1:1 correspondence ensures "
            "phase-locked coupling with zero mismatch at boundaries. The flux entering through "
            "any face exits through other faces with preserved phase relationships.\n\n"
            "The coherent rotation that results has measurable electromagnetic properties. "
            "The circulation creates a magnetic moment (the electron's intrinsic magnetism). "
            "The angular momentum quantization creates charge quantization (why charge comes "
            "in discrete units). The vortex topology creates stability (why electrons do not "
            "decay). All electromagnetic phenomena trace back to this fundamental vorticity "
            "in the gravitational field structure.\n\n"
            "This unification, electromagnetism emerging from gravitational vorticity, is "
            "the physical content of the triad mechanism. The Electric Field is gravity "
            "spinning in a coherent pattern."
        )
    },
    {
        "id": "vortex_stability_mechanics",
        "title": "Vortex Stability: Topological Protection of the Electron Pattern",
        "category": "Vortex Mechanics",
        "summary": "How the vortex eye provides topological anchoring for stable circulation.",
        "content": (
            "The electron vortex is stable because it is topologically protected. Once formed, "
            "the circulation pattern cannot smoothly unwind into a non-rotating state. This "
            "topological stability explains electron permanence: electrons do not decay, do not "
            "dissipate, and maintain their properties indefinitely.\n\n"
            "The protection comes from the vortex eye. At the center of the vortex (coinciding "
            "with the Field Origin), the radial gradient of the field reverses direction. "
            "Outside the eye, the field spirals inward; inside, the pattern inverts. This "
            "reversal point acts as a topological anchor. You cannot remove it by smooth "
            "deformation; doing so would require the field to be simultaneously flowing "
            "inward and outward at the same point, which is geometrically impossible.\n\n"
            "This is analogous to a knot in a rope. The knot cannot be undone by pulling "
            "on the ends; you must either cut the rope or physically manipulate the knot "
            "through itself. The vortex eye is the gravitational equivalent: a feature that "
            "cannot be smoothed away. The energy required to destroy the vortex (unbind the "
            "topological protection) is the electron rest mass, approximately 511 keV. This "
            "is not coincidence; it is the same energy scale as the compression blocking "
            "barrier, reflecting the deep connection between vortex stability and compression "
            "mechanics."
        )
    },
    
    # =========================================================================
    # SECTION VI: BINDING MECHANICS
    # =========================================================================
    {
        "id": "gravity_knot_formation_mechanics",
        "title": "Gravity Knot Formation: How Atoms Are Made",
        "category": "Binding Mechanics",
        "summary": "How gravity fields bind through the Field Origin to create atomic structure.",
        "content": (
            "Atoms ARE gravity knots: coupled configurations of gravity fields bound together "
            "through a shared Field Origin. The binding process has specific geometric "
            "requirements that explain both how atoms form and why certain configurations "
            "are stable while others are not.\n\n"
            "The process begins with unbound gravity fields approaching a host field under "
            "compression. The entering fields must be in the squish ball state (inward "
            "compression or no compression) to pass through the host's Field Origin. As "
            "they pass through, they enter Tetrahedron B, the even-parity tetrahedron "
            "inside the host's stellated octahedron structure.\n\n"
            "Once inside Tetrahedron B, the entering fields undergo spherical packing. They "
            "arrange themselves to minimize geometric stress, filling the available space "
            "according to the tetrahedral geometry. This packing triggers the bidirectional "
            "compression shift: the host field's compression reverses from inward to outward. "
            "The system transitions from squish ball to bowling ball state.\n\n"
            "The result is a gravity knot: a stable, topologically protected configuration. "
            "Like a knot in a rope, it cannot be smoothly untied. Separating the bound fields "
            "requires external energy to overcome the outward compression and reverse the "
            "bidirectional shift. This energy threshold is the binding energy, and it explains "
            "why atoms are stable: the bound state is energetically trapped."
        )
    },
    {
        "id": "spherical_packing_mechanics",
        "title": "Spherical Packing in Tetrahedron B: The Geometry of Nuclear Structure",
        "category": "Binding Mechanics",
        "summary": "How gravity fields arrange themselves within Tet B to form stable nuclei.",
        "content": (
            "When gravity fields bind, they pack into Tetrahedron B according to spherical "
            "packing rules. The geometry of this packing determines nuclear stability, "
            "explaining why certain mass numbers (k-multiples) form stable nuclei while "
            "others do not.\n\n"
            "Tetrahedron B has four vertices at even-parity positions, forming the geometric "
            "container for bound fields. When fields enter and pack, they occupy positions "
            "within this container. The occupancy count (how many fields are packed) equals "
            "the mass number A of the resulting atom. Each additional field changes the "
            "geometry of the packing.\n\n"
            "The key stability criterion is complete closure. With k=1 field in Tet B, you "
            "have point geometry (0D). With k=2, line geometry (1D). With k=3, plane geometry "
            "(2D). Only with k=4 do you achieve full tetrahedral geometry (3D), completing "
            "the closure. This is why helium-4 (A=4) is exceptionally stable: it represents "
            "the first complete 3D closure.\n\n"
            "Higher stable nuclei follow k-multiple rules. Carbon-12 (A=12 = 3k) has three "
            "nested tetrahedra that can pack coherently. Oxygen-16 (A=16 = 4k) has four. "
            "Iron-56 (A=56 = 14k) represents optimal packing efficiency. Configurations like "
            "A=8 = 2k fail because two complete tetrahedra cannot nest within a single Tet B "
            "structure."
        )
    },
    {
        "id": "hydrogen_configuration_mechanics",
        "title": "The (1+1) Hydrogen Configuration: Minimal Atomic Structure",
        "category": "Binding Mechanics",
        "summary": "How hydrogen achieves atomic identity with only one bound field.",
        "content": (
            "Hydrogen is the simplest atom: one host gravity field with one bound gravity "
            "field in its Tetrahedron B. This (1+1) configuration, where the first 1 is the "
            "host/container and the second 1 is the bound content, represents the minimal "
            "structure that qualifies as an atom.\n\n"
            "Despite having only k=1 occupancy in Tet B (point geometry with no 3D closure), "
            "hydrogen has the properties of an atom. The bidirectional compression shift "
            "has occurred: compression flows outward, making hydrogen a bowling ball that "
            "resists further compression. An electron vortex orbits the structure, bound "
            "to the central charge. The system is stable, with the bound field trapped by "
            "the outward compression barrier.\n\n"
            "The distinction between hydrogen (A=1) and empty spacetime (A=0) is fundamental. "
            "Empty spacetime has nothing in Tet B, no bidirectional shift has occurred, "
            "and compression flows inward. It is the medium through which atoms move, not "
            "an atom itself. Hydrogen has content, has shifted to outward compression, and "
            "has atomic identity. The single bound field makes all the difference.\n\n"
            "Hydrogen's k=1 geometry (a point) explains both its stability and its eagerness "
            "to bond. Point geometry has no 3D closure, leaving the structure geometrically "
            "incomplete. This incompleteness drives hydrogen to form molecules and compounds, "
            "seeking the fuller closure that comes with additional binding partners."
        )
    },
    
    # =========================================================================
    # SECTION VII: TRANSLATION MECHANICS
    # =========================================================================
    {
        "id": "uniform_spin_mechanics",
        "title": "Uniform Spin: The Universal Chirality Requirement",
        "category": "Translation Mechanics",
        "summary": "How same-spin orientation enables coupling while opposite spin causes annihilation.",
        "content": (
            "All gravity fields in the universe share the same spin direction (chirality). "
            "This is not coincidence but geometric necessity: only same-spin fields can "
            "couple coherently. Opposite-spin fields annihilate on contact.\n\n"
            "The mechanism involves complementary faces. When two same-spin fields approach, "
            "their faces present complementary configurations. FACE_A7 (with vertices summing "
            "to 7) meets FACE_B0 (with vertices summing to 14). These faces are bitwise "
            "complements: vertex 1 pairs with vertex 6, vertex 2 with vertex 5, vertex 4 "
            "with vertex 3. They interlock like a lock and key, enabling coupling.\n\n"
            "When opposite-spin fields approach, identical faces meet. FACE_A7 meets FACE_A7, "
            "or FACE_B0 meets FACE_B0. Identical faces cannot interlock; they collide. The "
            "result is destructive interference. Like two tornadoes spinning in opposite "
            "directions, sin + (-sin) = 0. The fields cancel, releasing energy in "
            "annihilation.\n\n"
            "This is why matter-antimatter annihilation occurs. Antimatter is matter with "
            "opposite chirality. When particle meets antiparticle, opposite-spin fields "
            "collide, faces fail to interlock, and the structures destroy each other. "
            "Uniform spin throughout our universe is why matter is stable: everything "
            "presents compatible faces for coupling."
        )
    },
    {
        "id": "spatial_translation_mechanics",
        "title": "Spatial Translation: How Atoms Move Through Space",
        "category": "Translation Mechanics",
        "summary": "How atoms traverse empty gravity fields through continuous coupling and decoupling.",
        "content": (
            "Atoms move through space by continuously coupling and decoupling with empty "
            "gravity fields. This spatial translation mechanism works because uniform spin "
            "ensures every empty field presents the correct complementary face for coupling.\n\n"
            "Consider an atom at position N, coupled to the empty gravity field at that "
            "location. The atom's FACE_A7 (outward-pointing from its Tet A apex) interlocks "
            "with the empty field's FACE_B0 (inward-pointing toward its Tet B). They are "
            "coupled, sharing a consistent geometry at their interface.\n\n"
            "As the atom moves, it decouples from field N and approaches field N+1. Because "
            "all fields share the same spin, field N+1 also presents FACE_B0 toward incoming "
            "objects. The atom's FACE_A7 interlocks with N+1's FACE_B0, and coupling occurs. "
            "The process repeats: N+1 to N+2 to N+3, indefinitely.\n\n"
            "This is like a train on tracks. The wheels (atom) always fit the rails (empty "
            "fields) because the geometry is universal. Every empty field is compatible with "
            "every atom. If spin were not uniform, some fields would present wrong-handed "
            "faces, like randomly switched rail gauges. Atoms would get stuck or annihilate "
            "randomly. Motion through space would be impossible.\n\n"
            "Empty gravity fields thus serve as the medium for motion. They are the tracks "
            "on which atoms travel, the substrate through which matter moves."
        )
    },
    
    # =========================================================================
    # SECTION VIII: THE STELLAR FORGE
    # =========================================================================
    {
        "id": "stellar_compression_mechanics",
        "title": "Stellar Compression: The Forge That Creates Elements",
        "category": "Stellar Forge",
        "summary": "How stellar cores provide the conditions for overcoming compression barriers.",
        "content": (
            "Stars are element factories. Their cores provide the sustained pressure and "
            "temperature needed to overcome compression blocking barriers, forcing gravity "
            "fields through Field Origins to create heavier elements. The stellar forge "
            "operates through a specific sequence of conditions.\n\n"
            "The process begins when a gas cloud exceeds the Jeans mass, the threshold where "
            "gravitational attraction overcomes thermal pressure. The cloud collapses, and "
            "as gravity fields approach each other, the core temperature rises. This "
            "temperature represents the kinetic energy of the compressed material.\n\n"
            "At ignition temperature (around 15 million Kelvin for hydrogen fusion), the "
            "thermal energy becomes sufficient to overcome the compression blocking barrier "
            "for some fraction of colliding nuclei. Atoms unbind, converting from bowling "
            "balls to squish balls. The unbound fields can now pass through Field Origins "
            "and re-bind as heavier elements. The binding releases energy (from the "
            "bidirectional shift), which maintains the temperature against cooling.\n\n"
            "In the stable furnace phase, radiation pressure from fusion balances gravitational "
            "collapse. The star reaches equilibrium, steadily converting hydrogen to helium "
            "for billions of years. When hydrogen is exhausted, the core contracts further, "
            "reaching temperatures sufficient to fuse helium into carbon. Each generation of "
            "fusion produces heavier elements until iron, where binding energy per nucleon "
            "peaks and fusion no longer releases net energy."
        )
    },
    {
        "id": "element_creation_mechanics",
        "title": "Element Creation: Building the Periodic Table",
        "category": "Stellar Forge",
        "summary": "How successive fusion generations construct heavier elements from hydrogen.",
        "content": (
            "The periodic table is built through successive generations of stellar fusion. "
            "Each generation creates heavier elements by packing more gravity fields into "
            "Tetrahedron B configurations, following k-multiple stability rules.\n\n"
            "First generation: Hydrogen to Helium. Four hydrogen nuclei (each 1+1 configuration) "
            "are compressed in the stellar core. Stellar energy unbinds them (bowling balls to "
            "squish balls), allowing all four to pass through a single Field Origin and pack "
            "into one Tet B. The result is helium-4 with complete k=4 closure. Binding energy "
            "released: 26.7 MeV per helium nucleus. This powers main sequence stars.\n\n"
            "Second generation: Helium to Carbon. Three helium-4 nuclei (each k=4) must combine "
            "to form carbon-12 (k=12 = 3x4). This is the triple-alpha process, requiring "
            "temperatures above 100 million Kelvin. It proceeds through a resonance because "
            "beryllium-8 (k=8 = 2x4) is unstable. Carbon-12 achieves stable nested tetrahedral "
            "geometry.\n\n"
            "Higher generations continue the pattern. Carbon fuses to oxygen (k=16), oxygen to "
            "silicon, silicon to iron (k=56 = 14x4). Iron marks the endpoint of fusion energy "
            "release; heavier elements require energy input and form primarily in supernovae. "
            "Each stable element represents a k-multiple configuration that achieves proper "
            "tetrahedral nesting within Tetrahedron B."
        )
    },
    {
        "id": "neutron_formation_mechanics",
        "title": "Electron Embedding: How Neutrons Form",
        "category": "Stellar Forge",
        "summary": "How extreme compression embeds the electron vortex inside the gravity field.",
        "content": (
            "Under extreme compression, the electron vortex can be pushed through the Field "
            "Origin and embedded inside the gravity field structure. This electron embedding "
            "is the geometric mechanism for neutron formation.\n\n"
            "Normally, the electron vortex orbits outside the Field Origin, bound to the "
            "central proton charge but not passing through the eye. The vortex eye and Field "
            "Origin are distinct locations in this configuration. But at extreme densities "
            "(around 10^11 kg/m^3, typical of neutron star material), the compression shrinks "
            "the electron orbit until it reaches the Field Envelope scale.\n\n"
            "At threshold, the vortex passes through the Field Origin. The gravity field "
            "effectively folds around the embedded electron, incorporating the vortex pattern "
            "into its internal structure. The result is a neutron: electrically neutral because "
            "the electron charge is now internal, with slightly higher mass than a proton "
            "because the embedding adds energy to the system.\n\n"
            "The process releases a neutrino, which carries away the lepton number and excess "
            "energy. This is the geometric interpretation of electron capture: not the "
            "destruction of an electron, but its embedding into the gravity field structure "
            "through the Field Origin gateway."
        )
    },
    
    # =========================================================================
    # SECTION IX: SCALE CONNECTIONS
    # =========================================================================
    {
        "id": "mond_transition_mechanics",
        "title": "The MOND Transition: How Field Closure Changes at Low Acceleration",
        "category": "Scale Connections",
        "summary": "How field closure dynamics shift at the characteristic acceleration a_0.",
        "content": (
            "Field closure operates differently at high and low accelerations, with the "
            "transition occurring at the MOND scale a_0 = 1.2 x 10^-10 m/s^2. This is not "
            "a modification of gravity but a change in how the k=4 closure channels fill.\n\n"
            "At high accelerations (well above a_0), all k=4 closure channels are fully "
            "engaged. The system operates in the Newtonian regime where the interpolating "
            "function mu(x) approaches 1. Gravity behaves as Newton described: inverse-square "
            "falloff, linear response to mass, no surprises.\n\n"
            "At low accelerations (well below a_0), the closure channels fill differently. "
            "The interpolating function mu(x) approaches x, giving effective gravity that "
            "falls off more slowly than inverse-square. This is the deep-MOND regime, "
            "responsible for flat galaxy rotation curves without requiring dark matter.\n\n"
            "The transition at a_0 is where mu(x) = 0.5, exactly halfway between the two "
            "regimes. The processing boundary r_c = sqrt(GM/a_0) marks this transition "
            "spatially. Inside r_c, closure operates approximately Newtonian. Outside r_c, "
            "closure transitions to the low-acceleration mode. For the Sun, r_c is about "
            "7000 AU; for galaxies, it typically lies within the visible disk."
        )
    },
    {
        "id": "cosmological_connection_mechanics",
        "title": "Cosmological Connection: Linking Field Envelope to Horizon",
        "category": "Scale Connections",
        "summary": "How the smallest gravitational structures connect to the cosmic horizon.",
        "content": (
            "The MOND acceleration scale a_0 connects the smallest gravitational structures "
            "(Field Envelopes at r_e = 2.82 fm) to the largest (the cosmic horizon at c/H). "
            "This connection suggests a deep relationship between local field geometry and "
            "universal dynamics.\n\n"
            "From field geometry: a_0 = k^2 (G m_e / r_e^2) = 16 G m_e / r_e^2. This expresses "
            "a_0 in terms of local quantities: the closure constant k, the electron mass m_e, "
            "and the Field Envelope scale r_e. No cosmological quantities appear.\n\n"
            "From horizon thermodynamics: a_0 = c H / (2 pi), where H is the Hubble parameter "
            "and c/H is the Hubble radius. This expresses a_0 in terms of cosmic quantities: "
            "the speed of light and the expansion rate of the universe. No local field "
            "quantities appear.\n\n"
            "That these two expressions give the same value (within measurement uncertainty) "
            "is remarkable. It implies that the field closure geometry encoded at femtometer "
            "scales somehow knows about the cosmic horizon at 10^26 meter scales. This is "
            "not coincidence but constraint: the same k=4 closure constant that determines "
            "local field structure also determines how the universe expands. Local and global "
            "are geometrically linked through the closure mechanism."
        )
    },
    {
        "id": "frame_correction_mechanics",
        "title": "Frame Correction: Reconciling Flat and Curved Descriptions",
        "category": "Scale Connections",
        "summary": "How sqrt(k/pi) converts between tetrahedral and spherical geometries.",
        "content": (
            "The Field Chamber has flat tetrahedral geometry characterized by k=4. The "
            "Field Envelope has curved spherical geometry characterized by pi. When making "
            "measurements that involve both descriptions, a frame correction factor "
            "sqrt(k/pi) = 1.128 reconciles them.\n\n"
            "The correction arises because the tetrahedron and sphere are different ways "
            "of enclosing the same volume. The tetrahedron has flat faces meeting at sharp "
            "edges and vertices. The sphere has continuous curvature everywhere. Their "
            "surface areas differ, their volumes differ, and measured quantities in each "
            "frame differ by the ratio of their characteristic constants.\n\n"
            "The Hubble parameter provides an example. Measured in the flat tetrahedral "
            "frame, H_flat reflects the closure geometry directly. Measured in the curved "
            "spherical frame (as astronomers actually do), H_measured differs by the frame "
            "correction: H_measured = H_flat / sqrt(k/pi). This correction appears whenever "
            "comparing the discrete, flat description of Field Chambers with the continuous, "
            "curved description of Field Envelopes.\n\n"
            "The frame correction is not a fudge factor but a geometric necessity. It "
            "encodes the relationship between the two complementary descriptions of the "
            "same underlying field structure."
        )
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_concept(concept_id):
    """Get a concept by its ID."""
    for c in GFD_CONCEPTS:
        if c["id"] == concept_id:
            return c
    return None


def get_concepts_by_category(category):
    """Get all concepts in a category."""
    return [c for c in GFD_CONCEPTS if c["category"] == category]


def get_all_concept_categories():
    """Get list of all unique categories."""
    return list(dict.fromkeys(c["category"] for c in GFD_CONCEPTS))


def search_concepts(query):
    """Search concepts by title or summary."""
    query = query.lower()
    results = []
    for c in GFD_CONCEPTS:
        if query in c["title"].lower() or query in c["summary"].lower():
            results.append(c)
    return results


# =============================================================================
# QUICK REFERENCE
# =============================================================================

def print_concept_reference():
    """Print a quick reference of all concepts."""
    categories = get_all_concept_categories()
    for cat in categories:
        print(f"\n{'='*70}")
        print(f"  {cat.upper()}")
        print(f"{'='*70}")
        for c in get_concepts_by_category(cat):
            print(f"\n  {c['title']}")
            print(f"  {'-'*60}")
            print(f"  {c['summary']}")


if __name__ == "__main__":
    print("Gravity Field Dynamics Concepts")
    print("=" * 50)
    print(f"Total concepts: {len(GFD_CONCEPTS)}")
    print(f"Categories: {len(get_all_concept_categories())}")
    print_concept_reference()
