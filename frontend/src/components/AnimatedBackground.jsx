/**
 * AnimatedBackground Component
 * Displays floating orbs with gradient background matching old project design
 */

export const AnimatedBackground = () => {
    return (
        <>
            <div className="animated-bg" />
            <div className="fixed inset-0 -z-10 opacity-10 pointer-events-none">
                {/* Floating Orb 1 */}
                <div
                    className="floating-orb"
                    style={{
                        width: '100px',
                        height: '100px',
                        top: '20%',
                        left: '10%',
                        animationDelay: '0s',
                    }}
                />

                {/* Floating Orb 2 */}
                <div
                    className="floating-orb"
                    style={{
                        width: '150px',
                        height: '150px',
                        top: '60%',
                        right: '15%',
                        animationDelay: '2s',
                    }}
                />

                {/* Floating Orb 3 */}
                <div
                    className="floating-orb"
                    style={{
                        width: '80px',
                        height: '80px',
                        bottom: '20%',
                        left: '70%',
                        animationDelay: '4s',
                    }}
                />
            </div>
        </>
    );
};
