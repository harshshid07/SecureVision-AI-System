/**
 * SecurityAlert Component
 * Alert item with colored border for dashboard
 */

export const SecurityAlert = ({
    type = 'info', // success, warning, danger, info
    title,
    message,
    timestamp,
}) => {
    const typeConfig = {
        success: {
            borderColor: 'border-green-500',
            icon: '✓',
            iconColor: 'text-green-400',
        },
        warning: {
            borderColor: 'border-yellow-500',
            icon: '⚠',
            iconColor: 'text-yellow-400',
        },
        danger: {
            borderColor: 'border-red-500',
            icon: '!',
            iconColor: 'text-red-400',
        },
        info: {
            borderColor: 'border-primary-blue',
            icon: 'ℹ',
            iconColor: 'text-primary-blue',
        },
    };

    const config = typeConfig[type] || typeConfig.info;

    return (
        <div className={`alert-item ${config.borderColor} p-3 mb-2 bg-dark-card rounded`}>
            <div className="flex items-start gap-2">
                <span className={`${config.iconColor} font-bold mt-1`}>
                    {config.icon}
                </span>
                <div className="flex-1">
                    <strong className="block text-dark-text">{title}</strong>
                    {message && (
                        <p className="text-sm text-dark-muted mb-0">{message}</p>
                    )}
                    {timestamp && (
                        <small className="text-xs text-dark-muted">
                            {new Date(timestamp).toLocaleString()}
                        </small>
                    )}
                </div>
            </div>
        </div>
    );
};
