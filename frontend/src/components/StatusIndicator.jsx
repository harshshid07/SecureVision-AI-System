/**
 * StatusIndicator Component
 * Pulsing status indicator dot
 */

export const StatusIndicator = ({
    active = true,
    className = '',
}) => {
    return (
        <span
            className={`status-indicator ${active ? 'status-active' : 'status-inactive'} ${className}`}
            title={active ? 'Active' : 'Inactive'}
        />
    );
};
