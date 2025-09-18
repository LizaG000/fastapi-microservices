using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public DbSet<UserEntity> Users { get; set; } = null!;

    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("user");

        modelBuilder.Entity<UserEntity>(entity =>
        {
            entity.ToTable("users");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.FirstName).IsRequired();
            entity.Property(e => e.LastName).IsRequired();
            entity.Property(e => e.Age).IsRequired();
            entity.Property(e => e.Number).IsRequired();
            entity.Property(e => e.Email).IsRequired();
        });
    }
}

public class UserEntity
{
    public int Id { get; set; }
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public int Age { get; set; }
    public string Number { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
}