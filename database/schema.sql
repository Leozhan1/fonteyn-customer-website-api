-- =============================================
-- Table: accounts
-- Description: User accounts for authentication
-- Date format for UDoB: YYYY-MM-DD
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.accounts') AND type in (N'U'))
BEGIN
    CREATE TABLE dbo.accounts (
        UID INT IDENTITY(1,1) PRIMARY KEY,
        FirstName VARCHAR(50) NOT NULL,
        LastName VARCHAR(50) NOT NULL,
        UPass VARCHAR(255) NOT NULL,
        UEmail VARCHAR(100) NOT NULL UNIQUE,
        URole VARCHAR(20) DEFAULT 'user',
        UDoB DATE
    );
END
GO

-- Add index on email for faster lookups
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_accounts_UEmail')
BEGIN
    CREATE INDEX IX_accounts_UEmail ON dbo.accounts(UEmail);
END
GO

-- =============================================
-- Table: tickets
-- Description: Booking tickets for parks/rooms
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.tickets') AND type in (N'U'))
BEGIN
    CREATE TABLE dbo.tickets (
        TID INT IDENTITY(1,1) PRIMARY KEY,
        UID INT NOT NULL,
        TAmount INT,
        TStart DATE,
        TEnd DATE,
        Timestamp DATETIME2 DEFAULT GETDATE(),
        TType VARCHAR(50),
        TPark VARCHAR(100),
        RoomID INT,
        PaymentAmount DECIMAL(10,2),
        CONSTRAINT FK_tickets_accounts FOREIGN KEY (UID) REFERENCES dbo.accounts(UID)
    );
END
GO

-- Add index on UID for faster user ticket lookups
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_tickets_UID')
BEGIN
    CREATE INDEX IX_tickets_UID ON dbo.tickets(UID);
END
GO

-- =============================================
-- Table: rooms
-- Description: Rooms available in the park
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.rooms') AND type in (N'U'))
BEGIN
    CREATE TABLE dbo.rooms (
        RoomID INT PRIMARY KEY,
        Location VARCHAR(100),
        RoomNumber VARCHAR(50),
        isOccupied BIT DEFAULT 0
    );
END
GO


-- =============================================
-- Table: login_attempts
-- Description: Audit log for login attempts
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.login_attempts') AND type in (N'U'))
BEGIN
    CREATE TABLE dbo.login_attempts (
        id INT IDENTITY(1,1) PRIMARY KEY,
        email VARCHAR(100),
        ip_address VARCHAR(50),
        success BIT,
        timestamp DATETIME2 DEFAULT GETDATE()
    );
END
GO
